
from collections import OrderedDict
from json import load
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from os.path import exists, join, getsize
from base.json_response import JSONResponse
from indx.version_convs import version_str2intrest, VersionTooHigh
from indx.models import PackageSeries, PackageVersion


def package_list(request):
	packages = PackageSeries.objects.filter(listed=True).prefetch_related('versions').order_by('pk')
	index = OrderedDict()
	for package in packages:
		versions = [pv.version_display for pv in package.versions.all()]
		if versions:
			index[package.name] = versions
	return JSONResponse(request, index)


def package_info(request, name):
	try:
		package = PackageSeries.objects.get(name=name)
	except PackageSeries.DoesNotExist:
		return HttpResponse('package "{0:s}" not found'.format(name), status=404)
	versions = {
		'versions': [pv.version_display for pv in package.versions.filter(listed=True)],
		'unlisted_versions': [pv.version_display for pv in package.versions.filter(listed=False)],
	}
	return JSONResponse(request, versions)


def version_info(request, name, v):
	try:
		package = PackageSeries.objects.get(name=name)
	except PackageSeries.DoesNotExist:
		return HttpResponse('package "{0:s}" not found'.format(name), status=404)
	try:
		vnr, rest = version_str2intrest(v)
		version = PackageVersion.objects.get(package=package, version=vnr, rest=rest)
	except PackageVersion.DoesNotExist:
		return HttpResponse('version "{1:s}" for package "{0:s}" not found'.format(name, v), status=404)
	except VersionTooHigh:
		return HttpResponse('version "{1:s}" for package "{0:s}" is too high'.format(name, v), status=400)
	versions = [pv.version_display for pv in package.versions.filter(listed=True)]
	if not exists(join(version.path, 'config.json')):
		return HttpResponse('package "{0:s}" version "{1:s}" appears to be damaged or missing'.format(name, v), status=500)
	with open(join(version.path, 'config.json'), 'r') as fh:
		info = load(fp = fh, object_pairs_hook = OrderedDict)
	download_url = reverse('version_download', kwargs={'name': package.name, 'v': version.version_display})
	ready = version.is_ready
	info['is_ready'] = ready
	if ready:
		info['download_url'] = join(settings.SITE_URL, download_url[1:])
		info['cdn_prefix'] = settings.CDN_URL
	info['versions'] = versions
	return JSONResponse(request, info)


def version_download(request, name, v):
	try:
		package = PackageSeries.objects.get(name=name)
	except PackageSeries.DoesNotExist:
		return HttpResponse('package "{0:s}" not found'.format(name), status=404)
	try:
		vnr, rest = version_str2intrest(v)
		version = PackageVersion.objects.get(package=package, version=vnr, rest=rest)
	except PackageVersion.DoesNotExist:
		return HttpResponse('version "{1:s}" for package "{0:s}" not found'.format(name, v), status=404)
	except VersionTooHigh:
		return HttpResponse('version "{1:s}" for package "{0:s}" is too high'.format(name, v), status=400)
	if not version.is_ready:
		return HttpResponse('package version is not ready, please wait', status=400)
	if settings.DEBUG:
		"""
			Serve the file through Django; only for development!
		"""
		response = HttpResponse(open(version.zip_path, 'br').read())
	else:
		"""
			Let Apache do the work by giving it a X-Sendfile header as authorization.
		"""
		response = HttpResponse('')
		response['X-Sendfile'] = version.zip_path
	response['Content-type'] = 'application/zip'
	response['Content-Disposition'] = 'attachment; filename="{0:s}"'.format(version.version_display)
	response['Content-Length'] = getsize(version.zip_path)
	return response


