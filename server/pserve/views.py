
from collections import OrderedDict
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from base.json_response import JSONResponse
from pindex.models import PackageSeries


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
	versions = [pv.version_display for pv in package.versions.all()]
	return JSONResponse(request, versions)


def version_info(request, name, version):
	pass


def dependency_tree(request, name, version):
	return HttpResponse(name)


