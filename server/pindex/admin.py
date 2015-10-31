
from django.contrib import admin
from pindex.forms import PackageVersionForm
from pindex.models import PackageSeries, PackageVersion


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


admin.site.register(PackageSeries, PackageSeriesAdmin)


