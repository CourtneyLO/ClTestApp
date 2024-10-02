"""Add Module Description"""

from django.contrib import admin

from main.admin import BaseAbstractAdmin
from .models import UserModel

class UserAdmin(BaseAbstractAdmin):
    """Add Class Description"""

    list_display = ('id', 'name', 'username', 'profile_picture')
    ordering = ('id', 'name', 'username', 'profile_picture')

admin.site.register(UserModel, UserAdmin)
