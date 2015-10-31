
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import IndexUser


admin.site.register(IndexUser, UserAdmin)


