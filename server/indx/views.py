
from collections import OrderedDict
from json import load
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from os.path import exists
from os.path import join
from base.json_response import JSONResponse
from pindex.functions import version_str2intrest, VersionTooHigh
from pindex.models import PackageSeries, PackageVersion


def package_list(request):
	packages = PackageSeries.objects.filter(listed=True).prefetch_related('versions').order_by('pk')
	index = OrderedDict()
	for package in packages:
		versions = [pv.version_display for pv in package.versions.all()]
		if versions:
			index[package.name] = versions
	return JSONResponse(request, index)


def package_redirect(request, name):
	try:
		package = PackageSeries.objects.get(name=name)
	except PackageSeries.DoesNotExist:
		return HttpResponse('package "{0:s}" not found'.format(name), status=404)
	return redirect(reverse('package_info', kwargs={'name': package.name}))


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
	# download url
	if not exists(join(version.path, 'config.json')):
		return HttpResponse('package "{0:s}" version "{1:s}" appears to be damaged or missing'.format(name, v), status=500)
	with open(join(version.path, 'config.json'), 'r') as fh:
		info = load(fp = fh, object_pairs_hook = OrderedDict)
	info['versions'] = versions
	info['download'] = ''
	info['cdn_prefix'] = ''
	return JSONResponse(request, info)



