"""
 This module is based on project Sensor-Andrew
 http://www.ices.cmu.edu/censcir/sensor-andrew/

 Most of the models are based on the revision 315 of http://sensor.andrew.cmu.edu:9000/
 and information published on the project wiki: # http://sensor.andrew.cmu.edu:9000/

 The schema is simplified and adapted to my requirements
 
"""
import time
import datetime

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db import models

import logging
logger = logging.getLogger(__name__)
logger.level = 20

version = '2016.05.29'

class Units(models.Model):
    """
    Table describing measurement units for specific measurements and physical signals the project
    """
    # SYSTEM_OF_UNITS = (
    #                    ('SI'    ,'SI'),
    #                    ('ENG'   ,'Imperial'),
    #                    ('NONE'  ,'None'),
    #                    ('AU'    ,'Arbitrary units'),
    #                    ('COUNTS','Digital counts'),
    #                    )
    
    #units_id     = models.AutoField(primary_key=True)    
    name   = models.CharField(max_length=25, default="None")
    symbol = models.CharField(max_length=30, blank=True)
    system = models.CharField(max_length=8, blank=True)
    notes  = models.TextField(blank=True)
        
    class Admin:
        pass
    
    def __unicode__(self):
        return "%s [%s]" % (self.name, self.symbol)

class Manufacturer(models.Model):
    name  = models.CharField(max_length=150, default="None")
    url   = models.URLField(max_length=750, blank=True)
    notes = models.TextField(blank=True)
        
    class Admin:
        pass
    
    def __unicode__(self):
        return self.name

class TimeStamp(models.Model):
    """
    Model describing events when the measurements were taken and when they were actually submitted to the server.
    In case of offline data loggers the time at which the measuremnt was taken will not be the same as the submission time.    
    """
    server_timestamp          = models.DateTimeField(auto_now_add=True)
    measurement_timestamp     = models.DateTimeField()
    measurement_timestamp_sec = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return str(self.measurement_timestamp)

    def save(self, *args, **kwargs):
        #do_something()
        self.measurement_timestamp_sec = round(time.mktime(self.measurement_timestamp.timetuple()))
        super(TimeStamp, self).save(*args, **kwargs) # Call the "real" save() method.        
        pass
        #do_something_else()

    def get_measurement_timestamp_in_ms(self):
        return time.mktime(self.measurement_timestamp.timetuple())*1000

    def get_measurement_timestamp_in_sec(self):
        return time.mktime(self.measurement_timestamp.timetuple())

    ms  = property(get_measurement_timestamp_in_ms)
    sec = property(get_measurement_timestamp_in_sec)
    
class PhysicalSignal(models.Model):
    """
    Description of the physical phenomenon being measured, such as air temperature, pressure, etc.
    """    
    signal_name        = models.CharField(max_length=25, default="None")
    signal_description = models.CharField(max_length=30, blank=True)        
    
    def __unicode__(self):
        return self.signal_name

class Device(models.Model):
    """
    protocol - describes com protocol between device and gateway
    """
    
    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, default = None)
    units        = models.ForeignKey(Units, null=True, blank=True, default = None)
    device_name  = models.CharField(max_length=225)
    update_rate  = models.DecimalField("Min. Update Interval [sec]",max_digits=15, decimal_places=3, default=1)    
    model_number = models.CharField(max_length=255, blank=True)
    actuator     = models.BooleanField(blank=True, default=False)
    protocol     = models.CharField("Protocol", max_length=255, blank=True)
    image_url    = models.URLField(blank=True)    
    transducer_type = models.TextField(blank=True)
    
    class Meta:
         unique_together = (("device_name", "model_number"),)
        
    def __unicode__(self):
        return "%s" % (self.device_name)

class DeviceGateway(models.Model):
    """
    Data acquisition board or interface board used to communicate with the measurement device
    
    protocol - describes com protocol between gateway and client node
    """
    name          = models.CharField("Name", max_length=255, default="localhost")
    address       = models.GenericIPAddressField("Address", default="127.0.0.1")
    port          = models.IntegerField("Port",default=8000)
    protocol      = models.CharField("Protocol", max_length=255, blank=True, default="http")
    url           = models.URLField(blank=True)
    mac_address   = models.CharField(max_length=75, blank=True)
    active        = models.BooleanField(default=True)
    process_name  = models.CharField("Process Name", max_length=255, blank=True)
    process_pid   = models.IntegerField("PID", default=0, blank=True)
    description   = models.CharField("Description", max_length=255, blank=True)
    #manufacturer  = models.ForeignKey(Manufacturer)    
    #serial_number = models.CharField("Serial Number", max_length=40, unique=True)
    
    def __unicode__(self):
        return self.name +"@"+ str(self.address)+":"+str(self.port)
     
class Location(models.Model):
    """
    Area where the device is installed, including absolute and relative coordinates of the device.  
    Absolute coordinates are referenced to the property origin, while relative xyz coordinates might might vary. 
    """
    area                   = models.TextField(default=None)    
    description            = models.TextField(blank=True)
    image_url              = models.URLField(blank=True);
    x_absolute             = models.DecimalField(max_digits=10, decimal_places=3, blank=True, default=0)
    y_absolute             = models.DecimalField(max_digits=10, decimal_places=3, blank=True, default=0)
    z_absolute             = models.DecimalField(max_digits=10, decimal_places=3, blank=True, default=0)    
    reference_description  = models.TextField(blank=True)
    x_reference            = models.DecimalField(max_digits=10, decimal_places=3, blank=True, default=0)
    y_reference            = models.DecimalField(max_digits=10, decimal_places=3, blank=True, default=0)
    z_reference            = models.DecimalField(max_digits=10, decimal_places=3, blank=True, default=0)
    
    def __unicode__(self):
        return "%s (%s)" % (self.area, self.description)

class DeviceInstance(models.Model): 
    user            = models.ForeignKey(User, related_name='device_instance', null=True, blank=True, default = None)
    device          = models.ForeignKey(Device, null=True, blank=True, default = None)    
    location        = models.ForeignKey(Location, null=True, blank=True, default=None)
    physical_signal = models.ForeignKey(PhysicalSignal, null=True, blank=True, default = None)    
    gateway         = models.ForeignKey(DeviceGateway, null=True, blank=True, default=None)    
    accept_from_gateway_only = models.BooleanField("From Gateway Only", default=False)
    
    serial_number   = models.CharField("Serial Number",max_length=255, unique=True)
    active          = models.BooleanField("Active",default=True)
    private         = models.BooleanField("Private",default=False)
    update_rate     = models.DecimalField("Min. Update [sec]",max_digits=15, decimal_places=3, default=1)
    update_rate_max = models.DecimalField("Max Update [sec]",max_digits=15, decimal_places=3, default=1)
    max_range       = models.DecimalField(max_digits=15, decimal_places=3, default=1)
    min_range       = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    update_threshold= models.DecimalField("Min. change in value to accept update",max_digits=15, decimal_places=3, default=0)
    callibration    = models.TextField(blank=True)
    description     = models.TextField(blank=True)
    
    def __unicode__(self):
        return "SN:{0}".format(self.serial_number)

    def save(self, *args, **kwargs):
        super(DeviceInstance, self).save(*args, **kwargs)
    
    def last_value(self):
        if self.datavalue_set.count() > 0:
            return self.datavalue_set.order_by('-data_timestamp')[0]
        else:
            return []

class DataValueManager(models.Manager):
    """"
    This method was replaced by last_value in DeviceInstance   
    def last(self, **kwargs):
       device_instance_queryset = DeviceInstance.objects.all().order_by('device')
       device_value_time = []
       for device_instance in device_instance_queryset:
           data_values = DataValue.objects.filter(device_instance=device_instance).order_by('data_timestamp')
           if len(data_values) > 1:
               val = data_values[0]
               device_value_time.append([device_instance, val])
               
       return device_value_time
    """ 
    def today(self, **kwargs):
        items = self.model.objects.filter(data_timestamp__measurement_timestamp__gte=datetime.date.today())
        return items

    def from_to(self, **kwargs):
        kwargs.has_key('from') and kwargs.has_key('to')
        start_date = datetime.datetime.strptime(kwargs['from'].split('.')[0],"%Y-%m-%d")
        end_date   = datetime.datetime.strptime(kwargs['to'].split('.')[0],"%Y-%m-%d")

        items = self.model.objects.filter(data_timestamp__measurement_timestamp__range=(start_date, end_date))
        return items

class DataValue(models.Model):
    """
    Class for storing single valued data, such as temperature, pressure, dac counts etc
    """
    data_timestamp  = models.ForeignKey(TimeStamp)    
    device_instance = models.ForeignKey(DeviceInstance)
    value           = models.FloatField()
    objects         = DataValueManager()

    def __unicode__(self):
        if self.data_timestamp_id == None:
            data_timestamp = 'none'
        else:
            data_timestamp = self.data_timestamp
        
        if self.device_instance_id == None:
            device_instance = 'none'
        else:
            device_instance = self.device_instance
        
        if self.value == None:
            value = 0
        else:
            value = self.value
                            
        return "%s: %f acquired with %s" % (data_timestamp, value, device_instance)

    def save(self, *args, **kwargs):
        super(DataValue, self).save(*args, **kwargs)

    def get_value_pair(self):
        #utc_time_ms = time.mktime(self.data_timestamp.measurement_timestamp.timetuple())*1000
        utc_time_ms = data_timestamp.measurement_timestamp_sec * 1000
        value       = self.value
        return [utc_time_ms, value]
    value_pair = property(get_value_pair)

class Experiment(models.Model):
    """
    Colleciton of measurements form a set of devices corresponding to an experiment
    """
    devices     = models.ManyToManyField(DeviceInstance)
    location    = models.ForeignKey(Location, null=True)
    description = models.TextField(blank=True)
    start_date  = models.DateTimeField()
    end_date    = models.DateTimeField()

##########################################################################
#
# Micro blog for the measurments
#
##########################################################################

class Note(models.Model):
    """
    model for keeping track of notes related to submitted data
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)    
    title      = models.CharField(max_length=255)
    slug       = models.SlugField(max_length=255, blank=True, default='')
    content    = models.TextField()    
    author     = models.ForeignKey(User, related_name="Note", default=1)
    
    class Meta:
        ordering = ["-created_at", "title"]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Note, self).save(*args, **kwargs)

    # @models.permalink
    # def get_absolute_url(self):
    #     return ("blog:detail", (), {"slug": self.slug})
        
##########################################################################
#
# UNDER CONSTRUCTION
#
##########################################################################
class DataObject(models.Model):
    """
    Class for storing serialized data objects
    format - specifies serializer, json, xml, csv, etc 
    """
    
    data_timestamp  = models.ForeignKey(TimeStamp)    
    device_instance = models.ForeignKey(DeviceInstance)
    value           = models.TextField(blank=True)
    format          = models.CharField(max_length=100, blank=True)
    
#    def __unicode__(self):
#        return "%s: acquired %s data with %s" % (data_timestamp, format, device_instance)

# class DataFile(models.Model):
#     """
#     Object used to deal with arbitrary data stored as a binary file and uploaded to the server.
#     This could be trace from scope, spectrometer or other instrument 
#     """
    
#     data_timestamp  = models.ForeignKey(TimeStamp)    
#     device_instance = models.ForeignKey(DeviceInstance)
#     binaryfiletype  = models.CharField(max_length=150)
#     path            = models.FileField(upload_to='/home/')
#     filename        = models.CharField(max_length=300, blank=True)
#     description     = models.TextField(blank=True)
#     credits         = models.CharField(max_length=750, blank=True)
    
#     class Meta:
#         pass
    
#     class Admin:
#         pass



    
# class DataValueSet(models.Model):
#      datavalue   = models.ManyToManyField(DataValue)
#      description = models.TextField(blank=True)
    