from django import forms
from .decorators import parsleyfy

class TextForm(forms.Form):
    name = forms.CharField(required=True)
    university = forms.CharField(required=False)

@parsleyfy
class TextForm2(forms.Form):
    name = forms.CharField(required=True)
    university = forms.CharField(required=False)

@parsleyfy
class FieldTypeForm(forms.Form):
    url = forms.URLField()
    url2 = forms.URLField(required=False)
    email = forms.EmailField()
    email2 = forms.EmailField(required=False)
