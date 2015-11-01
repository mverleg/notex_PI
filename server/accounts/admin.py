
from django.contrib.auth.admin import UserAdmin
from accounts.models import IndexUser
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from indx.models import PackageSeries


class PackageSeriesInline(admin.TabularInline):
	#form = PackageVersionForm
	model = PackageSeries
	extra = 1


class IndexUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
		(_('Packages'), {'fields': ('key',)}),
	)
	inlines = (PackageSeriesInline,)


admin.site.register(IndexUser, IndexUserAdmin)


