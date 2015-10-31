
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from os.path import join
from pindex.functions import version_intrest2str


class PackageSeries(models.Model):
	name = models.CharField(validators = [
		RegexValidator(settings.PACKAGE_NAME_PATTERN, 'Package names may contain only letters, numbers, periods and underscores and must start with a letter.'),
	], max_length=64, unique=True, db_index=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL) #todo
	license_name = models.CharField(max_length=32)
	readme_name = models.CharField(validators=[
		RegexValidator(r'^{0:s}$'.format(settings.FILENAME_PATTERN), settings.FILENAME_MESSAGE),
	], max_length=32, blank = True)
	listed = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Package'

	def __str__(self):
		return self.name


class PackageRequirement(models.Model):
	requirer = models.ForeignKey(PackageSeries, related_name='package_requirements')
	requirement = models.ForeignKey(PackageSeries, related_name='package_requirers')
	min = models.PositiveIntegerField(help_text='Minimum value (inclusive), filtering use only')
	max = models.PositiveIntegerField(help_text='Maximum vaue (inclusive), filtering use only')


class PackageVersion(models.Model):
	package = models.ForeignKey(PackageSeries, related_name='versions')
	version = models.PositiveIntegerField(help_text='10000 * major + minor')
	rest = models.CharField(validators=[
		RegexValidator(r'^[^.][a-zA-Z0-9_\-.]+$', 'Versions may contain only letters, numbers, periods, dashes and underscores.'),
	], max_length=24, blank=True)
	when = models.DateTimeField(auto_now_add=True)
	requires = models.ManyToManyField('self', related_name='required_by', through='PackageRequirement')
	listed = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Version'
		unique_together = ('package', 'version', 'rest')
		ordering = ('-when',)

	def __str__(self):
		return '{0:s}=={1:s}'.format(self.package.name, version_intrest2str(self.version, self.rest))

	@property
	def version_display(self):
		return version_intrest2str(self.version, self.rest)

	def path(self):
		return join(settings.PACKAGE_DIR, self.package.name, 'v{0:d}.{1.d}.')


