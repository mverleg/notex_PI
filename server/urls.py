
from django.conf.urls import include, url
from django.contrib import admin
import indx.urls


urlpatterns = [
	url(r'^index/', include(indx.urls)),
	url(r'^admin/', include(admin.site.urls)),
]


