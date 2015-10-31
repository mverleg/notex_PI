
from django.conf.urls import include, url
from django.contrib import admin
import pserve.urls


urlpatterns = [
	url(r'^index/', include(pserve.urls)),
	url(r'^admin/', include(admin.site.urls)),
]


