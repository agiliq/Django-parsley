import re

from django import forms
from parsley.decorators import parsleyfy
from .models import Student


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
    income2 = forms.FloatField()
    topnav = forms.RegexField(regex="#[A-Fa-f0-9]{6}")
    topnav2 = forms.RegexField(regex=re.compile("#[a-z]+", re.IGNORECASE))
    some_num = forms.IntegerField(min_value=10, max_value=100)
    amount = forms.DecimalField(max_digits=12, decimal_places=2, required=True, max_value=999999999999.99, min_value=-999999999999.99)


@parsleyfy
class ExtraDataForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    email2 = forms.EmailField()
    hide_errors = forms.CharField()

    class Meta:
        parsley_extras = {
            "name": {
                "error-message": "Name invalid",
            },
            "email2": {
                "equalto": "email",
                "equalto-message": "Must match",
            },
            "hide_errors": {
                "show-errors": False,
            },
        }


class ExtraDataMissingFieldForm(ExtraDataForm):
    def __init__(self, *args, **kwargs):
        del self.base_fields['email2']
        super(ExtraDataMissingFieldForm, self).__init__(*args, **kwargs)


@parsleyfy
class FormWithWidgets(forms.Form):
    description = forms.CharField(widget=forms.TextInput)
    blurb = forms.CharField(widget=forms.TextInput(attrs={
        "class": "highlight"}))

@parsleyfy
class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentModelForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.instance.name:
            self.name = "Luke Skywalker"
        return super(StudentModelForm, self).save(*args, **kwargs)

@parsleyfy
class FormWithCustomInit(forms.Form):
    description = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(FormWithCustomInit, self).__init__(*args, **kwargs)
        self.fields["description"].initial = "Hello"



class FormWithCleanField(forms.Form):
    description = forms.CharField(widget=forms.TextInput)

    def clean_description(self):
        raise forms.ValidationError("Error")


def get_state_choices():
    return [("NY", "NY"), ("OH", "OH")]

@parsleyfy
class FormWithCustomChoices(forms.Form):
    state = forms.ChoiceField(widget=forms.Select(choices=[]))
    def __init__(self, *args, **kwargs):
        super(FormWithCustomChoices, self).__init__(*args, **kwargs)
        self.fields['state'] = forms.ChoiceField(
            choices=get_state_choices())

@parsleyfy
class FormWithRadioSelect(forms.Form):
    state = forms.ChoiceField(choices=get_state_choices(), widget=forms.RadioSelect)


@parsleyfy
class FormWithRadioSelectNotRequired(forms.Form):
    state = forms.ChoiceField(choices=get_state_choices(), required=False, widget=forms.RadioSelect)


@parsleyfy
class FormWithMedia(forms.Form):
    name = forms.CharField(required=True)

    class Media:
        js = ("jquery.min.js",)
        css = {"all": ("jquery.css",)}


@parsleyfy
class FormWithoutMedia(forms.Form):
    name = forms.CharField(required=True)


class SSNWidget(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        kwargs['widgets'] = [
            forms.TextInput(),
            forms.TextInput(),
            forms.TextInput(),
            ]
        super(SSNWidget, self).__init__(*args, **kwargs)

    def decompress(self, value):
        return value.split('-') if value else [None, None, None]


class SSN(forms.MultiValueField):
    widget = SSNWidget
    def __init__(self, *args, **kwargs):
        fields = (
            forms.RegexField(r'^(\d)+$', min_length=3, max_length=3),
            forms.RegexField(r'^(\d)+$', min_length=3, max_length=3),
            forms.RegexField(r'^(\d)+$', min_length=4, max_length=4),
        )
        super(SSN, self).__init__(fields=fields, *args, **kwargs)


@parsleyfy
class MultiWidgetForm(forms.Form):
    ssn = SSN()


@parsleyfy
class CustomErrorMessageForm(forms.Form):
    name = forms.CharField(error_messages={"max_length": "Please only 30 characters"}, max_length=30, required=False)
    email = forms.EmailField(error_messages={"invalid": "Invalid email"}, required=False)
    favorite_color = forms.CharField(error_messages={"required": "Favorite color is required"})


@parsleyfy
class CustomPrefixForm(forms.Form):
    name = forms.CharField(required=True)

    class Meta:
        parsley_namespace = 'custom'
