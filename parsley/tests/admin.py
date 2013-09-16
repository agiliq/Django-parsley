from django.contrib import admin

from parsley.mixins import ParsleyAdminMixin

from .models import Student


class StudentAdmin(ParsleyAdminMixin, admin.ModelAdmin):
    pass
