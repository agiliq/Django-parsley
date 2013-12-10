from django import forms
from parsley.decorators import parsleyfy
from core.models import Profile

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
class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile