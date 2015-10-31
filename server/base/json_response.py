
from json import dumps
from django.conf import settings
from django.http import HttpResponse


class JSONResponse(HttpResponse):
	def __init__(self, request, data, indent = 2 if settings.DEBUG else None, status_code = 200, content_type = 'application/json', mime = None, **json_kwargs):
		if mime is not None:
			content_type = mime
		content = dumps(data, indent = indent, **json_kwargs)
		super(JSONResponse, self).__init__(content = content, content_type = content_type, status = status_code)


