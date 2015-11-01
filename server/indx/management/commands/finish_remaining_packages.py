
from django.core.management import BaseCommand
from indx.upload import upload_postproc, test_queue
from indx.models import PackageVersion


class Command(BaseCommand):
	help = 'Goes through all package versions and queues zip tasks for any non-ready ones'

	def handle(self, *args, **options):
		for version in PackageVersion.objects.all():
			if not version.is_ready:
				print('adding {0:s} to queue'.format(version))
				upload_postproc(version)
		print('done!')


