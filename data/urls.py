from django.conf.urls import patterns, url
from django.conf.urls import include

import views
import data

#from rest_framework import serializers, viewsets, routers
#import rest
# Serializers define the API representation.

# Routers provide a way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'dev', rest.DeviceInstanceViewSet)
# router.register(r'user', rest.UserViewSet)
# router.register(r'group', rest.GroupViewSet)

urlpatterns = patterns('',
    url(r'^$',views.HomePageView.as_view(), name='sensordata_home'),
    url(r'^ping$',data.views.ping, name='sensordata_ping'),    
    
    ## SUBMIT DATA
    url(r'^submit/(?P<datestamp>now)/sn/(?P<sn>.*)/(?P<mode>\w{3})/(?P<val>.*)$',\
        'data.api_views.api_submit_datavalue', name='api_submit_datavalue_now'),

    url(r'^submit/(?P<datestamp>\d{4}\-\d{1,2}\-\d{1,2}-\d{1,2}:\d{1,2}:\d{1,2}\.*\d{0,6})/sn/(?P<sn>.*)/(?P<mode>\w{3})/(?P<val>.*)$',\
        'data.api_views.api_submit_datavalue', name='api_submit_datavalue_timestamp'),

	## GET DATA
    url(r'^sn/(?P<serial_number>[a-zA-Z0-9-_\.]+)/$', views.api_get_data),
    url(r'^sn/(?P<serial_number>[a-zA-Z0-9-_\.]+)/(?P<today>today)/$', views.api_get_data),    
    url(r'^sn/(?P<serial_number>[a-zA-Z0-9-_\.]+)/from/(?P<from>\d{4}\-\d{1,2}\-\d{1,2})/to/(?P<to>\d{4}\-\d{1,2}\-\d{1,2})/$',views.api_get_data),

    ## REST API
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)