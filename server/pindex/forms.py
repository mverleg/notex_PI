
from django import forms
from django.core.validators import RegexValidator
from pindex.functions import version_str2intrest, version_intrest2str


# class PackageRequirementForm(forms.ModelForm):
#
# 	min_str = forms.CharField(label='min', validators = [
# 		RegexValidator(r'^\d+(?:\.\d+)?$', 'Version range limits should be formatted like 1.0.'),
# 	], required=False, help_text='Lower limit, inclusive')
# 	max_str = forms.CharField(label='max', validators = [
# 		RegexValidator(r'^\d+(?:\.\d+)?$', 'Version range limits should be formatted like 1.0.'),
# 	], required=False, help_text='Upper limit, inclusive; use \'inf\' for no upper limit')
# 	requirement = forms.ModelChoiceField(label='requirement', queryset=PackageSeries.objects.all())
#
# 	class Meta:
# 		fields = ('requirement',)
#
# 	def __init__(self, *args, instance = None, **kwargs):
# 		super(PackageRequirementForm, self).__init__(*args, instance = instance, **kwargs)
# 		self.fields['min_str'].widget.attrs['placeholder'] = '1.0'
# 		self.fields['max_str'].widget.attrs['placeholder'] = 'inf'
# 		if instance:
# 			self.fields['min_str'].initial = version_int2str(instance.min)
# 			self.fields['max_str'].initial = version_int2str(instance.max)
# 			self.fields['requirement'].queryset = PackageSeries.objects.exclude(pk = instance.requirer.pk)
# 		elif PackageRequirementForm.obj:
# 			self.fields['requirement'].queryset = PackageSeries.objects.exclude(pk = PackageRequirementForm.obj.pk)
#
# 	def clean(self):
# 		assert self.instance
# 		cleaned_data = super(PackageRequirementForm, self).clean()
# 		cdmin, cdmax = cleaned_data.get('min_str', '0.0'), cleaned_data.get('max_str', 'inf')
# 		self.instance.min = version_str2int(cdmin)
# 		#if self.instance.requirer.pk == self.instance.requirement.pk:
# 		#	raise ValidationError('A package cannot depend on itself.')
# 		if cdmax.startswith('inf'):
# 			self.instance.max = version_getmax()
# 		else:
# 			self.instance.max = version_str2int(cdmax)


class PackageVersionForm(forms.ModelForm):

	version_str = forms.CharField(label='Version', validators = [
		RegexValidator(r'^\d{1,4}(?:\.\d{1,4}(?:\.[^.][a-zA-Z0-9_\-.]+)?)?$', 'Version numbers should be formatted like 1.0.dev7, the first two being under 10,000.'),
	])

	class Meta:
		fields = ('listed',)

	def __init__(self, *args, instance = None, **kwargs):
		super(PackageVersionForm, self).__init__(*args, instance = instance, **kwargs)
		self.fields['version_str'].widget.attrs['placeholder'] = 'enter version'
		if instance:
			self.fields['version_str'].initial = version_intrest2str(instance.version, instance.rest)

	def clean(self):
		assert self.instance
		cleaned_data = super(PackageVersionForm, self).clean()
		if 'version_str' in cleaned_data:
			self.instance.version, self.instance.rest = version_str2intrest(cleaned_data['version_str'].lstrip('v'))


