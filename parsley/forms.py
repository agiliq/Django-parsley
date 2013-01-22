from django import forms
from .decorators import parsleyfy

class TextForm(forms.Form):
    name = forms.CharField(required=True,)
    university = forms.CharField(required=False)

@parsleyfy
class TextForm2(forms.Form):
    name = forms.CharField(required=True)
    university = forms.CharField(required=False)

@parsleyfy
class FieldTypeForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=30)
    url = forms.URLField()
    url2 = forms.URLField(required=False)
    email = forms.EmailField()
    email2 = forms.EmailField(required=False)
    age = forms.IntegerField()
    income = forms.DecimalField()

@parsleyfy
class FormWithWidgets(forms.Form):
    description = forms.CharField(widget=forms.TextInput)
    blurb = forms.CharField(widget=forms.TextInput(attrs={"class": "highlight"}))