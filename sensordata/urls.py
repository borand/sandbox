from django.conf.urls import patterns, url
from django.conf.urls import include
import views
import sensordata

urlpatterns = patterns('',
    url(r'^$',views.HomePageView.as_view(), name='sensordata_home'),
    url(r'^ping$',sensordata.views.ping, name='sensordata_ping'),
)