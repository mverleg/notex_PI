
from django.conf import settings
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from indx.views import package_list, package_redirect, package_info, version_info, version_download


urlpatterns = [
    # url(r'^$', lambda request: redirect(reverse('package_list'))),
    # url(r'^\*$'.format(settings.PACKAGE_NAME_PATTERN), package_list, name = 'package_list'),
    # url(r'^(?P<name>{0:s})/?$'.format(settings.PACKAGE_NAME_PATTERN), package_redirect),
    # url(r'^(?P<name>{0:s})/\*/info$'.format(settings.PACKAGE_NAME_PATTERN), package_info, name = 'package_info'),
    # url(r'^(?P<name>{0:s})/(?P<v>[^.][a-zA-Z0-9_\-.]+)/info$'.format(settings.PACKAGE_NAME_PATTERN), version_info, name = 'version_info'),
    # url(r'^(?P<name>{0:s})/(?P<v>[^.][a-zA-Z0-9_\-.]+)/download'.format(settings.PACKAGE_NAME_PATTERN), version_download, name = 'version_info'),
]


