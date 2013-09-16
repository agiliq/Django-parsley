from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from parsley.admin import ParsleyMixin


class MyUserAdmin(ParsleyMixin, UserAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
