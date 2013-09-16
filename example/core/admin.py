from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from parsley.mixins import ParsleyAdminMixin


class MyUserAdmin(ParsleyAdminMixin, UserAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
