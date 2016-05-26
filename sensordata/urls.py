from django.conf.urls import patterns, url
from django.conf.urls import include
from rest_framework import serializers, viewsets, routers

import views
import sensordata
import rest
# Serializers define the API representation.

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'dev', rest.DeviceInstanceViewSet)
router.register(r'user', rest.UserViewSet)
router.register(r'group', rest.GroupViewSet)

urlpatterns = patterns('',
    url(r'^$',views.HomePageView.as_view(), name='sensordata_home'),
    url(r'^ping$',sensordata.views.ping, name='sensordata_ping'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)