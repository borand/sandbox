# Create your views here.
from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.views.generic import ListView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from data.models import DeviceInstance, DataValue, TimeStamp
import json

import datetime
import time
from data_utils import data_value_submission
import logging
logger = logging.getLogger(__name__)

class ApiDeviceInstanceView(ListView):    
    model = DeviceInstance
    

class ApiDataValueView(TodayArchiveView):
    model = TimeStamp
    queryset = TimeStamp.objects.all()
    date_field = "measurement_timestamp"
    make_object_list = True
    allow_future = True
    
    