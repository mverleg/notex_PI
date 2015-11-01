
from django.contrib.auth.admin import UserAdmin
from accounts.models import IndexUser
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class IndexUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
		(_('Packages'), {'fields': ('key', 'packages')}),
	)


admin.site.register(IndexUser, IndexUserAdmin)


