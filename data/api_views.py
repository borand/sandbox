# native libraries
import time
import datetime

# django libraries
from django.http import Http404
from django.contrib.auth.models import User
from django.http import HttpResponse
from . import models
from data_utils import data_value_submission
import logging
logger = logging.getLogger(__name__)

# rest_framework libraries

#######################################################################################
# API - usign django-rest-framework
#

#######################################################################################
# API
#

def api_submit_datavalue(request, datestamp, sn, val, mode):
    msg = "[SUBMITTED] datestamp: %s, sn: %s, val: %s, mode=%s" % (datestamp, sn, val, mode)
    print(msg)
    logger.info(msg)

    try:
    	if "obj" in mode:
        	is_obj = True
    	else:
        	is_obj = False
        results = data_value_submission(datestamp, sn, val, request.META.get('REMOTE_ADDR'),is_obj)
    except Exception as E:                
        results = 'Exception:' + E.message
    return HttpResponse(results)