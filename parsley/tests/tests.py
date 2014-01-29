import re
import six

from django import forms
from django.contrib import admin
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from parsley.decorators import parsleyfy

from .forms import (TextForm, TextForm2, FieldTypeForm, ExtraDataForm,
        ExtraDataMissingFieldForm, FormWithWidgets, StudentModelForm,
        FormWithCleanField, FormWithCustomInit, FormWithCustomChoices,
        FormWithMedia, FormWithoutMedia, MultiWidgetForm, CustomErrorMessageForm,
        CustomPrefixForm)
from .models import Student
from .admin import StudentAdmin


class ParsleyTestCase(TestCase):

    def assertAttrsEqual(self, a, b):
        for k in a.keys():  # ignore unspecified keys
            if k in b:
                if six.PY3:
                    x, y = str(a[k]), str(b[k])
                else:
                    x, y = unicode(a[k]), unicode(b[k])
                self.assertEqual(x, y)


class CharFieldTest(ParsleyTestCase):
    def test_basic(self):
        """
        Tests that parsleyfy will add parsley-required for required fields,
        but not for required=False fields for CharFields
        """
        form = TextForm()
        self.assertEqual(form.fields["name"].widget.attrs, {})
        self.assertEqual(form.fields["university"].widget.attrs, {})
        ParsleyForm = parsleyfy(TextForm)
        form = ParsleyForm()
        self.assertAttrsEqual(form.fields["name"].widget.attrs, {
            "parsley-required": "true",
            "parsley-required-message": _("This field is required.")
        })
        self.assertEqual(form.fields["university"].widget.attrs, {})


class CharFieldDecoratedTest(ParsleyTestCase):
    def test_decorated(self):
        "Tests that parsleyfy works as a class Decorator"
        form = TextForm2()
        self.assertAttrsEqual(form.fields["name"].widget.attrs, {
            "parsley-required": "true",
            "parsley-required-message": _("This field is required.")
        })
        self.assertEqual(form.fields["university"].widget.attrs, {})


class FieldTypeFormTest(ParsleyTestCase):
    def test_fields(self):
        "Tests that parsleyfy adds parsley-required for things other than CharField"
        form = FieldTypeForm()
        fields = form.fields
        self.assertEqual(fields["url"].widget.attrs["parsley-required"], "true")
        self.assertFalse("parsley-required" in fields["url2"].widget.attrs)
        self.assertEqual(fields["email"].widget.attrs["parsley-required"], "true")
        self.assertFalse("parsley-required" in fields["email2"].widget.attrs)


class DataTypeTest(ParsleyTestCase):
    def test_data_types(self):
        "Test that different field types get correct parsley-type"
        form = FieldTypeForm()
        fields = form.fields
        self.assertTrue("parsley-type" in fields["url"].widget.attrs)
        self.assertEqual(fields["url"].widget.attrs["parsley-type"], "url")
        self.assertTrue("parsley-type" in fields["email"].widget.attrs)
        self.assertEqual(fields["email"].widget.attrs["parsley-type"], "email")
        self.assertEqual(fields["age"].widget.attrs["parsley-type"], "digits")
        self.assertEqual(fields["income"].widget.attrs["parsley-type"], "number")
        self.assertEqual(fields["income2"].widget.attrs["parsley-type"], "number")
        self.assertEqual(fields["topnav"].widget.attrs["parsley-regexp"], "#[A-Fa-f0-9]{6}")
        self.assertNotIn("parsley-regexp-flag", fields["topnav"].widget.attrs)
        self.assertEqual(fields["topnav2"].widget.attrs["parsley-regexp"], "#[a-z]+")
        self.assertEqual(fields["topnav2"].widget.attrs["parsley-regexp-flag"], "i")


class LengthTest(ParsleyTestCase):
    def test_length(self):
        form = FieldTypeForm()
        fields = form.fields
        name_attrs = fields["name"].widget.attrs
        self.assertTrue("parsley-minlength" in name_attrs)
        self.assertEqual(name_attrs["parsley-minlength"], 3)
        self.assertEqual(name_attrs["parsley-maxlength"], 30)


class ValueTest(ParsleyTestCase):
    def test_value(self):
        form = FieldTypeForm()
        fields = form.fields
        num_attrs = fields['some_num'].widget.attrs
        self.assertTrue("parsley-min" in num_attrs, True)
        self.assertTrue("parsley-max" in num_attrs, True)
        self.assertEqual(num_attrs["parsley-min"], 10)
        self.assertEqual(num_attrs["parsley-max"], 100)


class FormWithWidgetsTest(ParsleyTestCase):
    def test_widgets(self):
        "Assert that @parsleyfy doesn't cloober existing attrs"
        form = FormWithWidgets()
        self.assertTrue(form.fields["description"].widget, forms.TextInput)
        self.assertEqual("highlight", form.fields["blurb"].widget.attrs["class"])


class TestMetadata(ParsleyTestCase):
    def test_docstring(self):
        form1 = TextForm()
        form2 = parsleyfy(TextForm)()
        self.assertEqual(form1.__doc__, form2.__doc__)

    def test_module(self):
        form1 = TextForm()
        form2 = parsleyfy(TextForm)()
        self.assertEqual(form1.__module__, form2.__module__)

    def test_name(self):
        form1 = TextForm()
        form2 = parsleyfy(TextForm)()
        self.assertEqual(form1.__class__.__name__, form2.__class__.__name__)


class TestModelForm(ParsleyTestCase):
    def test_model_form(self):
        form = StudentModelForm()
        fields = form.fields
        foo_attrs = fields["name"].widget.attrs
        self.assertEqual(foo_attrs["parsley-required"], "true")

    def test_model_form_save(self):
        form = StudentModelForm({"name": "Luke Skywalker"})
        form.save(commit=False)


class TestCustomInit(ParsleyTestCase):
    def test_custom_init(self):
        form = FormWithCustomInit()
        self.assertEqual(form.fields["description"].initial, "Hello")

    def test_custom_choices(self):
        form = FormWithCustomChoices()
        self.assertNotEqual(len(form.fields['state'].choices), 0)
        self.assertEqual(form.fields['state'].choices,
                    [("NY", "NY"), ("OH", "OH")])


class TestCleanFields(ParsleyTestCase):
    def test_clean(self):
        form = FormWithCleanField(data={"description": "foo"})
        self.assertEqual(form.is_bound, True)
        self.assertEqual(form.is_valid(), False)
        self.assertTrue(hasattr(form, "clean_description"))

    def test_clean_parslyfied(self):
        form = parsleyfy(FormWithCleanField)(data={"description": "foo"})
        self.assertEqual(form.is_bound, True)
        self.assertEqual(form.is_valid(), False)
        self.assertTrue(hasattr(form, "clean_description"))


class TestExtraAttributes(ParsleyTestCase):
    def test_equalto(self):
        form = ExtraDataForm()
        attrs = form.fields["email2"].widget.attrs
        self.assertAttrsEqual(attrs, {
            "parsley-type": "email",
            "parsley-required": "true",
            "parsley-equalto-message": "Must match",
            "parsley-equalto": "#id_email",
            "parsley-required-message": _("This field is required."),
        })

    def test_default_data(self):
        form = ExtraDataForm()
        attrs = form.fields["name"].widget.attrs
        self.assertAttrsEqual(attrs, {
            "parsley-required": "true",
            "parsley-error-message": "Name invalid",
            "parsley-required-message": _("This field is required.")
        })

    def test_boolean_values(self):
        form = ExtraDataForm()
        attrs = form.fields["hide_errors"].widget.attrs
        self.assertAttrsEqual(attrs, {
            "parsley-required": "true",
            "parsley-show-errors": "false",
            "parsley-required-message": _("This field is required.")
        })

    def test_missing_field(self):
        ExtraDataMissingFieldForm()  # No error should be raised


class TestMultiValueField(ParsleyTestCase):
    def test_parsley_attributes(self):
        form = MultiWidgetForm()
        fields = form.fields["ssn"].fields
        self.assertAttrsEqual(fields[0].widget.attrs, {
            "parsley-minlength": 3,
            "parsley-maxlength": 3,
            "maxlength": "3",
            "parsley-regexp": r'^(\d)+$',
        })
        self.assertAttrsEqual(fields[1].widget.attrs, {
            "parsley-minlength": 3,
            "parsley-maxlength": 3,
            "maxlength": "3",
            "parsley-regexp": r'^(\d)+$',
        })
        self.assertAttrsEqual(fields[2].widget.attrs, {
            "parsley-minlength": 4,
            "parsley-maxlength": 4,
            "maxlength": "4",
            "parsley-regexp": r'^(\d)+$',
        })


class TestCustomErrorMessages(TestCase):

    def test_new_message(self):
        form = CustomErrorMessageForm()
        attrs = form.fields['name'].widget.attrs
        self.assertEqual(attrs, {
            "maxlength": '30',
            "parsley-maxlength": 30,
            "parsley-maxlength-message": "Please only 30 characters"
        })

    def test_field_type_message(self):
        form = CustomErrorMessageForm()
        attrs = form.fields['email'].widget.attrs
        self.assertEqual(attrs, {
            "parsley-type": "email",
            "parsley-type-email-message": "Invalid email"
        })

    def test_override_default_message(self):
        form = CustomErrorMessageForm()
        attrs = form.fields['favorite_color'].widget.attrs
        self.assertEqual(attrs, {
            "parsley-required": "true",
            "parsley-required-message": "Favorite color is required"
        })

class TestCustomPrefix(TestCase):

    def test_default_prefix(self):
        form = TextForm()
        attrs = form.fields['name'].widget.attrs
        self.assertTrue('parsley-required' in attrs)

    def test_custom_prefix(self):
        form = CustomPrefixForm()
        attrs = form.fields['name'].widget.attrs
        self.assertTrue('custom-required' in attrs)
