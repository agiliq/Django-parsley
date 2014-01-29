from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from parsley.mixins import ParsleyAdminMixin


class MyUserAdmin(ParsleyAdminMixin, UserAdmin):

    class Media:
        js = (
            "//code.jquery.com/jquery-latest.min.js",
            "parsley/js/parsley.min.js",
            "parsley/js/parsley.django-admin.js"
        )


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
