from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

import main.views
import data.urls

urlpatterns = [
    url(r'^$', main.views.index, name='index'),    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include(data.urls, namespace="data")),
]
