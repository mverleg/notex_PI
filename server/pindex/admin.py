
from django.contrib import admin
from pindex.forms import PackageVersionForm, PackageRequirementForm
from pindex.models import PackageSeries, PackageVersion, PackageRequirement


class PackageVersionInline(admin.TabularInline):
	form = PackageVersionForm
	model = PackageVersion
	extra = 1


class PackageSeriesAdmin(admin.ModelAdmin):
	list_display = ('name', 'owner', 'listed', 'license_name',)
	list_filter = ('owner', 'listed', 'license_name',)
	inlines = (PackageVersionInline,)

	class Media:
		css = {'all' : ('admin_inline_model_name_hack.css',) }


class PackageRequirementInline(admin.TabularInline):
	form = PackageRequirementForm
	model = PackageRequirement
	fk_name = 'requirer'
	extra = 3

	def get_formset(self, request, obj=None, **kwargs):
		"""
			This is a bad idea (race condition) but it's the only way.
			See http://stackoverflow.com/questions/22466594/django-get-instance-in-inline-form-admin
		"""
		PackageRequirementForm.obj = obj
		return super(PackageRequirementInline, self).get_formset(request, obj, **kwargs)


class PackageVersionAdmin(admin.ModelAdmin):
	list_display = ('version_display', 'package', 'listed', 'version', 'when',)
	list_filter = ('package', 'listed', 'version', 'when',)
	inlines = (PackageRequirementInline,)

	class Media:
		css = {'all' : ('admin_inline_model_name_hack.css',) }


admin.site.register(PackageSeries, PackageSeriesAdmin)
admin.site.register(PackageVersion, PackageVersionAdmin)


