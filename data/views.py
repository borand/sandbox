import time
import datetime
import json

# Create your views here.
from django.contrib.auth import authenticate, login
from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView
from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.utils.log import getLogger
from data import models

import logging
logger = logging.getLogger(__name__)
#########################################################################
#
# Group of Home views
#
def ping(request):
    msg = "pong %s" % (datetime.datetime.now())
    logger.info(msg)    
    return HttpResponse(msg)

class HomePageView(TemplateView):
    template_name = "home.html"
    def get_context_data( **kwargs):

        msg = "Sensordata app loaded @ %s" % (datetime.datetime.now())
        context = super(HomePageView, self).get_context_data(**kwargs)        
        context['msg'] = msg
        logger.info(msg)
        return context

def api_submit_datavalue(request, datestamp, sn, val, mode):
    msg = "[SUBMITTED] datestamp: %s, sn: %s, val: %s" % (datestamp, sn, val)
    logger.info(msg)
    try:
        if "obj" in mode:
            is_obj = True
        else:
            is_obj = False

        results = data_value_submission(datestamp, sn, val, request.META.get('REMOTE_ADDR'), is_obj)
    except Exception as E:                
        results = ' Exception: ' + E.message
    return HttpResponse(results)

def api_get_data(request, **kwargs):
    print(kwargs)
    logger.debug('get_queryset(kwargs= %s)' % str(kwargs))
    to = time.time()    

    serial_number = kwargs['serial_number']
    queryset = models.DataValue.objects.filter(device_instance__serial_number=serial_number).order_by('data_timestamp__measurement_timestamp')
    logger.debug("Query time             = %.3f" % (time.time() - to))        
    
    if kwargs.has_key('today'):
        logger.debug("Filtering: todays data")        
        queryset = queryset.filter(data_timestamp__measurement_timestamp__gte=datetime.date.today())

    if kwargs.has_key('from') and kwargs.has_key('to'):
        logger.debug("Filtering: from %s to %s" % (kwargs.has_key('from'), kwargs.has_key('to')))
        start_date = datetime.datetime.strptime(kwargs['from'].split('.')[0],"%Y-%m-%d")
        end_date   = datetime.datetime.strptime(kwargs['to'].split('.')[0],"%Y-%m-%d")
        queryset = queryset.filter(data_timestamp__measurement_timestamp__range=(start_date, end_date))

    logger.debug("Found %d items matching criteria " % queryset.count())
    values_list = queryset.values_list('data_timestamp__measurement_timestamp_sec','value')    
    #v = queryset.values_list('value',flat=True)
    #t = queryset.values_list('data_timestamp__measurement_timestamp',flat=True)
    logger.debug("Making the list        = %.3f" % (time.time() - to))

    logger.debug("Preparing array for json transmision")
    data = []
    for data_pt in values_list:        
        data.append([data_pt[0],data_pt[1]])
    
    kwargs['data'] = data;
    kwargs['name'] = serial_number;
    kwargs['name'] = serial_number;
    kwargs['query_time'] = time.time() - to;
    json_data = json.dumps(kwargs)
    print("Making value pair list = %.3f" % (time.time() - to))    
    return HttpResponse(json_data)
