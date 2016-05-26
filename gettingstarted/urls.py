from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sensordata/', include('sensordata.urls', namespace="sensordata")),

    ## SUBMIT DATA
    url(r'^submit/(?P<datestamp>now)/sn/(?P<sn>.*)/(?P<mode>\w{3})/(?P<val>.*)$',\
        'sensordata.api_views.api_submit_datavalue', name='api_submit_datavalue_now'),

    url(r'^submit/(?P<datestamp>\d{4}\-\d{1,2}\-\d{1,2}-\d{1,2}:\d{1,2}:\d{1,2}\.*\d{0,6})/sn/(?P<sn>.*)/(?P<mode>\w{3})/(?P<val>.*)$',\
        'sensordata.api_views.api_submit_datavalue', name='api_submit_datavalue_timestamp'),
]
