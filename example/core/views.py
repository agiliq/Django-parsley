from django.views.generic.edit import FormView

from core.forms import FieldTypeForm


class HomeView(FormView):
    template_name = "home.html"
    form_class = FieldTypeForm
    success_url = '/'
