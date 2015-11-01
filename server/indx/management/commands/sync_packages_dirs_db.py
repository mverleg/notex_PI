
from os import walk
from json import load
from django.conf import settings
from django.core.management import BaseCommand
from os.path import join
from re import compile
from django.db.transaction import atomic
from indx.upload import upload_postproc
from indx.version_convs import version_str2intrest
from indx.models import PackageVersion, PackageSeries


class Command(BaseCommand):
	help = 'Goes through all packages and adds any database entries that are missing'

	def create_instances(self, to_create, obj_map):
		made = []
		for create in to_create:
			with open(join(settings.PACKAGE_DIR, create, 'config.json')) as fh:
				conf = load(fp = fh)
			checkname = '{0:s}/v{1:s}'.format(conf['name'], conf['version'])
			assert create == checkname, 'filename and config do not match! path: {0:s} config: {1:s}'.format(create, checkname)
			if not conf['name'] in obj_map:
				package = PackageSeries(name=conf['name'], owner=None, license_name=conf.get('license', '?'), readme_name=conf.get('readme', ''), listed=False)
				package.save()
				obj_map[conf['name']] = package
			else:
				package = obj_map[conf['name']]
			vnr, rest = version_str2intrest(conf['version'])
			pv = PackageVersion(package=package, version=vnr, rest=rest, listed=False)
			pv.save()
			made.append(pv)
		return made

	@atomic
	def delete_instances(self, to_delete, obj_map):
		for delete in to_delete:
			obj_map[delete].delete()

	def get_dir_packages(self):
		"""
			Find directories with configs.
		"""
		pattern = '^{0:s}$'.format(join(
			settings.PACKAGE_DIR,
			'({0:s})'.format(settings.PACKAGE_NAME_PATTERN),
			'(v\d+\.\d+(?:\.{0:s})?)'.format(settings.VERSION_REST_PATTERN),
			'config.json',
		))
		dirs = []
		regx = compile(pattern)
		for k, parts in enumerate(walk(settings.PACKAGE_DIR, followlinks=True)):
			for fname in parts[2]:
				found = regx.findall(join(parts[0], fname))
				if found:
					dirs.append('/'.join(found[0]))
		dirs = set(dirs)
		print('found {0:d} package directories'.format(len(dirs)))
		return dirs

	def get_db_entries(self):
		"""
			Find database entries.
		"""
		insts = []
		pvs = PackageVersion.objects.prefetch_related('package')
		for pv in pvs:
			nm = '{0:s}/v{1:s}'.format(pv.package.name, pv.version_display)
			insts.append(nm)
		insts = set(insts)
		print('found {0:d} package version instances'.format(len(insts)))
		return insts

	def handle(self, *args, **options):
		print('please wait...')
		"""
			Find instances to be created.
		"""
		dirs = self.get_dir_packages()
		insts = self.get_db_entries()
		creates = dirs - insts
		deletes = insts - dirs
		package_objs = {obj.name: obj for obj in PackageSeries.objects.all()}
		print('creating {0:d} instances'.format(len(creates)))
		versions = self.create_instances(creates, package_objs)
		print('preparing the instances (queue)')
		for version in versions:
			upload_postproc(version)
		print('cleaning up {0:d} instances'.format(len(deletes)))
		self.delete_instances(deletes, package_objs)
		print('done!')


