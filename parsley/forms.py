from django import forms

class TextForm(forms.Form):
    name = forms.CharField(required=True)