
from django.core.urlresolvers import resolve, Resolver404


class WwwSlashMiddleware():
	"""
		Combination of RemoveWwwMiddleware and AppendSlashMiddleware
	"""
	def process_request(self, request):
		original = request.build_absolute_uri()
		nw = original.replace('//www.', '//')
		if nw.endswith('/'):
			try:
				# use full path here instead of absolute uri; resolve doesn't handle domain names
				resolve(request.get_full_path()[:-1])
			except Resolver404:
				""" Version without / at the end doesn't exist - do not redirect. """
			else:
				nw = nw[:-1]
		if not original == nw:
			from django.http import HttpResponsePermanentRedirect
			return HttpResponsePermanentRedirect(nw)


