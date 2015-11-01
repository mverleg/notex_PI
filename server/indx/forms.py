
from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from package_versions import nrrest2str, str2nrrest


class PackageVersionForm(forms.ModelForm):

	version_str = forms.CharField(label='Version', validators = [
		RegexValidator(settings.VERSION_PATTERN, settings.VERSION_MESSAGE),
	])

	class Meta:
		fields = ('listed',)

	def __init__(self, *args, instance = None, **kwargs):
		super(PackageVersionForm, self).__init__(*args, instance = instance, **kwargs)
		self.fields['version_str'].widget.attrs['placeholder'] = 'enter version'
		if instance:
			self.fields['version_str'].initial = nrrest2str(instance.version, instance.rest)

	def clean(self):
		assert self.instance
		cleaned_data = super(PackageVersionForm, self).clean()
		if 'version_str' in cleaned_data:
			self.instance.version, self.instance.rest = str2nrrest(cleaned_data['version_str'])


