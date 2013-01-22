from django import forms
from .decorators import parsleyfy

class TextForm(forms.Form):
    name = forms.CharField(required=True)
    university = forms.CharField(required=False)

@parsleyfy
class TextForm2(forms.Form):
    name = forms.CharField(required=True)
    university = forms.CharField(required=False)
