
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from os.path import join, exists
from package_versions import nrrest2str


class PackageSeries(models.Model):
	name = models.CharField(validators = [
		RegexValidator(settings.PACKAGE_NAME_PATTERN, settings.PACKAGE_NAME_MESSAGE),
	], max_length=64, unique=True, db_index=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=True, related_name='packages')
	license_name = models.CharField(max_length=32)
	readme_name = models.CharField(validators=[
		RegexValidator(r'^{0:s}$'.format(settings.FILENAME_PATTERN), settings.FILENAME_MESSAGE),
	], max_length=32, blank = True)
	listed = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Package'

	def __str__(self):
		return self.name

	def get_absolute_path(self):
		return reverse('package_info', kwargs={'name': self.name})


class PackageVersion(models.Model):
	package = models.ForeignKey(PackageSeries, related_name='versions')
	version = models.PositiveIntegerField(help_text='10000 * major + minor')
	rest = models.CharField(validators=[
		RegexValidator(r'^{0:s}$'.format(settings.VERSION_REST_PATTERN), settings.VERSION_MESSAGE),
	], max_length=24, blank=True)
	when = models.DateTimeField(auto_now_add=True)
	listed = models.BooleanField(default=True)
	signature = models.CharField(max_length=43, help_text='b64 sha256 hash of the package')

	#todo: can not be approved if the license isn't one of the approved ones

	class Meta:
		verbose_name = 'Version'
		unique_together = ('package', 'version', 'rest')
		ordering = ('-version',)

	def __str__(self):
		return '{0:s}=={1:s}'.format(self.package.name, self.version_display)

	@property
	def version_display(self):
		return nrrest2str(self.version, self.rest)

	@property
	def path(self):
		return join(settings.PACKAGE_DIR, self.package.name, '{0:s}'.format(self.version_display))

	@property
	def zip_path(self):
		return join(settings.PACKAGE_ZIP_DIR, self.package.name, '{0:s}.zip'.format(self.version_display))

	@property
	def is_ready(self):
		return exists(self.zip_path)

	def get_absolute_path(self):
		return reverse('version_info', kwargs={'name': self.name, 'v': self.version_display})


class VersionApproval(models.Model):
	approver = models.ForeignKey(settings.AUTH_USER_MODEL)
	version = models.ForeignKey(PackageVersion)
	message = models.TextField(blank=True, null=True)
	when = models.DateTimeField(auto_now_add=True)


