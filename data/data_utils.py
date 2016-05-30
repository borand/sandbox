"""
This module contains 2 key function used in data submission:
"""
import datetime
import json
import logging
from data import models
from django.utils import timezone

logger = logging.getLogger(__name__)
logger.level = 20

def get_existing_or_new(date_string, save=False):
    """
    Attempts to find the existing TimeStamp object in the databasse
    (exact match down to a second) if none found creates 
    """
    logger.debug("get_existing_or_new(date_string=%s, save=%d)" % (date_string, save))        
    
    if 'now' in date_string:
        datetime_obj = timezone.now()
    else:
        datetime_obj = datetime.datetime.strptime(date_string.split('.')[0], "%Y-%m-%d-%H:%M:%S")

    logger.debug("submited time: %s" % str(datetime_obj))

    time_stamp = models.TimeStamp.objects.filter(measurement_timestamp__exact=datetime_obj)

    if len(time_stamp) == 0:
        logger.debug("no previous record with this timestamp found")
        time_stamp = models.TimeStamp()
        time_stamp.measurement_timestamp = datetime_obj
        if save:
            time_stamp.save()
    else:
        logger.debug("found existing record with this timestamp")
        time_stamp = time_stamp[0]

    return time_stamp

def data_value_submission(datestamp, serial_number, data_value, remote_addr, is_obj=False):
    """
    Handles submission of data from remote sensors into the data base.
    """
    
    msg = "  data_value_submission(%s, %s, %s, %s)" % (datestamp, serial_number, data_value, remote_addr)
    print(msg)
    logger.debug(msg)

    res = dict()
    res['status']     = 'REJECTED'
    res['accepted']   = False
    res['datestamp']  = datestamp
    res['is_obj']     = is_obj
    res['data_value'] = data_value
    res['from']       = remote_addr
    res['sn']         = serial_number
    res['delta_time_sec'] = -1;
    res['msg']        = "NOT FOUND IN DB"

    # Check to see if we have a valid data to work with 
    if is_obj:
        try:
            submitted_obj = json.loads(data_value)
        except Exception as E:
            msg = "cannot decode submited data as json. Error msg: " + E.message
            logger.debug(msg)
            res['msg'] = msg
            return json.dumps(res)
    else:
        try:
            data_value_float = float(data_value)
        except ValueError:
            msg = "Cannot convert to float attempting"            
            logger.debug(msg)
            res['msg'] = msg
            return json.dumps(res)

    # Check if the serial number is in our DB
    DeviceInstanceList = models.DeviceInstance.objects.filter(serial_number=serial_number)
    if len(DeviceInstanceList) == 0:
        msg = 'Device not found in DB'
        logger.debug(msg)
        res['msg'] = msg
        print(msg)
        return json.dumps(res)
    DeviceInstance = DeviceInstanceList[0]
    
    # Check for restrictions, that is if submission is only accepted from a given IP 
    if DeviceInstance.accept_from_gateway_only:
        msg = 'remote_address=%s matches DeviceInstance.gateway.address=%s' % (remote_addr, DeviceInstance.gateway.address)
        logger.debug(msg)
        if remote_addr not in DeviceInstance.gateway.address:
            msg = 'ip address not registered for data submit'
            logger.debug(msg)
            res['msg'] = msg
            print(msg)
            return json.dumps(res)

    # Check if the device is active 
    if not DeviceInstance.active:
        msg = "Device is not active, data will not be saved"
        logger.debug(msg)
        res['msg'] = msg
        print(msg)
        return json.dumps(res)
    
    # Check for submission with fugure date 
    TimeStamp = get_existing_or_new(datestamp)    
    if TimeStamp.measurement_timestamp > datetime.datetime.now():
        msg = 'Cannot submit values with future dates'        
        logger.debug(msg)
        res['msg'] = msg
        print(msg)
        return json.dumps(res)
    res['datestamp']  = TimeStamp.__unicode__()

    max_value   = float(DeviceInstance.max_range)
    min_value   = float(DeviceInstance.min_range)
    update_rate = float(DeviceInstance.update_rate)

    if is_obj == False:

        if data_value_float > max_value or data_value_float < min_value:
            msg = "Value submitted is out of range [{0} {1}]".format(min_value, max_value)
            logger.debug(msg)
            res['msg'] = msg
            print(msg)
            return json.dumps(res)

        ExistingDataValue = models.DataValue.objects.filter(device_instance=DeviceInstance).order_by('-data_timestamp')
        logger.debug("Found %d existing ExistingDataValue objects" % (ExistingDataValue.count()))

        if ExistingDataValue.count() > 0:
            delta_time            = TimeStamp.measurement_timestamp - ExistingDataValue[0].data_timestamp.measurement_timestamp
            delta_time_sec        = float(delta_time.seconds)
            last_data_value_float = ExistingDataValue[0].value
        else:
            delta_time_sec        = update_rate
            last_data_value_float = 10e10

        res['delta_time_sec'] = delta_time_sec;
        logger.debug("%d sec since last submisison" % (delta_time_sec))
        if delta_time_sec < update_rate:
            msg = "Maximum update rate = %d sec exceeded." % (update_rate)
            logger.debug(msg)        
            res['msg'] = msg
            print(msg)
            return json.dumps(res)
            
        if len(ExistingDataValue.filter(value=data_value_float, data_timestamp=TimeStamp)) > 0:
            msg = "Identical record already found in the data base, new submission rejected"
            logger.debug(msg)
            res['msg'] = msg
            print(msg)
            return json.dumps(res)        
        
        if abs(data_value_float - last_data_value_float) >= DeviceInstance.update_threshold or delta_time_sec > DeviceInstance.update_rate_max:
            TimeStamp.save()
            DataValueInstance = models.DataValue(value=data_value_float,
                                                 data_timestamp=TimeStamp,
                                                 device_instance=DeviceInstance)
            #DataValueInstance.save(using='data')
            DataValueInstance.save()
            msg = "value accepted and saved"
            logger.debug(msg)
            res['status']   = 'ACCEPTED'
            res['accepted'] = True
            res['msg']      = msg
            print(msg)
            return json.dumps(res)
        else:
            msg = "value submitted did not change by minimum threshold {0} withing {1} sec".format(DeviceInstance.update_threshold, DeviceInstance.update_rate_max)
            logger.debug(msg)        
            res['msg']      = msg
            print(msg)
            return json.dumps(res)
    else:
        logger.debug("Decoded submitted_obj")
        ExistingDataValue = models.DataObject.objects.filter(device_instance=DeviceInstance).order_by('-data_timestamp')
        logger.debug("Found %d existing ExistingDataValue objects" % (ExistingDataValue.count()))
        
        if ExistingDataValue.count() > 0:
            delta_time = TimeStamp.measurement_timestamp - ExistingDataValue[0].data_timestamp.measurement_timestamp
            delta_time_sec = float(delta_time.seconds)
        else:
            delta_time_sec = update_rate

        logger.debug("%d sec since last submisison" % (delta_time_sec))
        if delta_time_sec < update_rate:
            msg = "[REJECTED]: Maximum update rate = %d sec exceeded." % (update_rate)
        else:
            TimeStamp.save()
            DataValueInstance = models.DataObject(value=data_value, \
                                                   data_timestamp=TimeStamp, \
                                                   device_instance=DeviceInstance, \
                                                   format="JSON")
            DataValueInstance.save()
            msg = "value accepted and saved"
            logger.debug(msg)
            res['status']   = 'ACCEPTED'
            res['accepted'] = True
            res['msg']      = msg
            print(msg)
            return json.dumps(res)

if __name__ == '__main__':
    pass
    
