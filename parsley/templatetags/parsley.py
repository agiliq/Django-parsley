from django import template, VERSION

from ..decorators import parsley_form

register = template.Library()

if VERSION[:2] >= (1, 9):
    # in django 1.9 and above, the simple_tag can do assignment
    tag_decorator = register.simple_tag
else:
    # django 1.8 and below needs the assignment_tag
    tag_decorator = register.assignment_tag


@tag_decorator()
def parsleyfy(form):
    return parsley_form(form)
