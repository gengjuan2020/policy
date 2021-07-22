from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserInfo,Permission,Role
from django.utils.translation import gettext, gettext_lazy as _
# Register your models here.

admin.site.register(Permission)
admin.site.register(Role)

class UserAdmininfo(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('roles'), {'fields': ('roles',)}),
    )

admin.site.register(UserInfo,UserAdmininfo)