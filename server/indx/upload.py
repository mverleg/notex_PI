
from os import makedirs
from shutil import make_archive, move
from os.path import join
from time import sleep
from django.conf import settings
from django_q import Stat
from indx.models import PackageVersion
from django_q.tasks import async


def testing_func(): #todo: doesn't work, remove
	sleep(1)
	return 'test passed'


def test_queue(): # todo: doesn't work; remove
	async('indx.upload.testing_func')
	print(Stat.get_all())
	for stat in Stat.get_all():
		print(stat.cluster_id, stat.status)


def upload_postproc(version):
	"""
	1. Clean up any extra files.
	2. Create a zip file.
	"""
	async('indx.upload.create_zip', version.pk)


def create_zip(version_id):
	try:
		version = PackageVersion.objects.get(pk=version_id)
	except PackageVersion.DoesNotExist:
		raise PackageVersion.DoesNotExist('Trying to create archive of version pk={0:d} but it was not found'.format(version_id))
	package = version.package
	source_dir_path = join(settings.PACKAGE_DIR, package.name, '{0:s}'.format(version.version_display))
	goal_dir_path = join(settings.PACKAGE_ZIP_DIR, package.name)
	tmp_path = join(goal_dir_path, 'tmp.{0:s}'.format(version.version_display))
	file_path = join(goal_dir_path, '{0:s}.zip'.format(version.version_display))
	makedirs(goal_dir_path, exist_ok=True)
	make_archive(tmp_path, 'zip', root_dir=source_dir_path)
	move(tmp_path + '.zip', file_path)
	return version_id


#todo: well there's not really anything to do at this point
# def create_zip_ready(task):
# 	version_id = task.result
# 	try:
# 		version = PackageVersion.objects.get(pk=version_id)
# 	except PackageVersion.DoesNotExist:
# 		raise PackageVersion.DoesNotExist('Trying to get results of zipping version pk={0:d} but the isntance was not found'.format(version_id))
# 	print(version)

