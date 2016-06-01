"""daq.py -
module used to listen for new data on the redis channel and submit the data to Django managed DB

https://www.stavros.io/posts/standalone-django-scripts-definitive-guide/
"""
# Standard Lib imports
import threading
import datetime
import time
import json as sjson
import os, sys

proj_path= os.path.dirname(os.path.abspath(__file__)) + "/.."
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
print(proj_path)
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# PIP libraries
from redis import Redis
from redislog import handlers, logger

# Project libraries imports
from data import models
from data import api_views
from data import data_utils
from utils import hwcal

def submit_test():  
    out = data_utils.data_value_submission(datestamp="now", serial_number="0", data_value=0.5, remote_addr="127.0.0.1", is_obj=False)
    print(out)

##########################################################################################
class SubmitData(object):

    def __init__(self, channel=['data','MSG']):
        self.redis     = Redis()
        self.config    = dict()
        self.state     = dict()

        self.config['channel']  = channel
        self.config['print']    = False

        self.state['msg_count'] = 0;
        self.state['busy']      = False;        
        self.state['alive']     = False
        self.state['last']      = []

        self.pubsub    = self.redis.pubsub()        
        self.log       = logger.RedisLogger('daq.py:SubmitData')
        self.log.addHandler(handlers.RedisHandler.to("log", host='localhost', port=6379))
        self.log.level = 10
        
        self._subscribe_thread = False
        
        self.pubsub.subscribe(self.config['channel'])
        self.log.info("Initialized SubmitData()")
        self.start()

    def __del__(self):        
        self.log.info('__del__()')
        if self.subscribe_thread.is_alive():
            self.stop()

    def start(self):
        """Start reader thread"""
        self.log.debug("Start reader thread")        
        self.subscribe_thread    = threading.Thread(target=self.reader)
        self.subscribe_thread.setDaemon(True)
        self.subscribe_thread.start()

    def stop(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self.log.debug("Stop reader thread only, wait for clean exit of thread")
        self.redis.publish(self.config['channel'][0],"KILL")
        self._subscribe_thread = False
        self.subscribe_thread.join(3)

    def reader(self):
        self.log.debug('run()')
        self.state['alive'] = True
        self._subscribe_thread   = True

        while self._subscribe_thread:

            for item in self.pubsub.listen():
                self.state['last_item'] = item
                if item['data'] == "KILL":
                    self.pubsub.unsubscribe()
                    self.log.info("unsubscribed and finished")
                    return
                if item['data'] == "ERROR_TEST":
                    self.redis.publish('error', __name__ + ": ERROR_TEST")
                else:
                    if item['type'] == 'message':                                 
                        self.process_message(item)                    

        self.log.debug('end of reader() function')

    def process_message(self, item):
        self.log.debug('process_message()')
        try:
            if item['channel'] == 'data':
                device_data = [sjson.loads(item['data'])]
                timestamp   = "now"
                #timestamp   = datetime.datetime.strptime(timestamp.split('.')[0], "%Y-%m-%d-%H:%M:%S")
            if item['channel'] == 'MSG':
                msg         = sjson.loads(item['data'])
                tmp         = sjson.loads(msg['MSG']['data'])
                device_data = tmp['data']
                timestamp   = msg['MSG']['timestamp']

            self.state['device_data'] = device_data
            self.state['timestamp']   = timestamp

            for data in device_data:
                sn                  = data[0]
                device_instance     = models.DeviceInstance.objects.filter(serial_number__exact=sn)
                #print(device_instance)
                if device_instance.count() == 1:
                    reload(hwcal)
                    callibration = device_instance[0].callibration
                    self.state['callibration']   = callibration
                    processing_function = vars(hwcal)[callibration]
                    val                 = processing_function(data)
                else:
                    val = data[1]
                
                self.state['submit_sn_val']  = [timestamp, sn, val]
                submit_results = data_utils.data_value_submission(datestamp=timestamp, serial_number=sn, data_value=val, remote_addr="127.0.0.1", is_obj=False)                
                self.state['submit_results']  = submit_results
                self.state['msg_count'] += 1

                submit_dict = sjson.loads(submit_results)
                msg = "sn: {0:<25} val: {1:<10} status: {2}".format(submit_dict['sn'], submit_dict['data_value'],submit_dict['msg'])
                self.log.debug(msg)

                if self.config['print']:                    
                    print(msg)


        except Exception as E:
            self.log.error("process_message(): " + E.message)
            self.log.error(item)
            self.state['process_message_error'] = E

def StartIqrSubmit():    
    try:
        I = SubmitData();
        print("===============================================")
        while True:
            time.sleep(1)
            pass
    except KeyboardInterrupt:
        pass
    I.stop()
    del(I)

    print "Exiting " + __name__

##########################################################################################
if __name__ == "__main__":    
    StartIqrSubmit()
