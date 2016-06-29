from django import template
from ..decorators import parsley_form

register = template.Library()


@register.assignment_tag()
def parsleyfy(form):
    return parsley_form(form)
