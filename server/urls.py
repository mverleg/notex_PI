
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse
import indx.urls
import accounts.urls


urlpatterns = [
	url(r'^$', lambda request: HttpResponse('homepage')),
	url(r'^@dmin/', include(admin.site.urls)),
	url(r'^~', include(accounts.urls)),
	url(r'^', include(indx.urls)),
]


