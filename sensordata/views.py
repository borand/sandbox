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
from sensordata import models

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

    def get_context_data(self, **kwargs):

        msg = "Sensordata app loaded @ %s" % (datetime.datetime.now())
        context = super(HomePageView, self).get_context_data(**kwargs)
        # context['device_instance'] = models.DeviceInstance.objects..filter(private=False).order_by('device')
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