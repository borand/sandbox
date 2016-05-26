import time

from django.contrib.auth.models import User
from django.forms import widgets
#from django.utils.log import getLogger

from rest_framework import serializers

from .models import Units, Location, Manufacturer, TimeStamp, DataValue,\
                    DeviceInstance, PhysicalSignal, Device, DeviceGateway

#logger = getLogger("app")
import logging
logger = logging.getLogger(__name__)
#######################################################################################

