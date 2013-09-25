import re

from django import forms
from django.contrib import admin
from django.test import TestCase

from parsley.decorators import parsleyfy

from .forms import (TextForm, TextForm2, FieldTypeForm, ExtraDataForm,
        ExtraDataMissingFieldForm, FormWithWidgets, StudentModelForm,
        FormWithCleanField, FormWithCustomInit, FormWithCustomChoices,
        FormWithMedia, FormWithoutMedia, MultiWidgetForm)
from .models import Student
from .admin import StudentAdmin


class CharFieldTest(TestCase):
    def test_basic(self):
        """
        Tests that parsleyfy will add data-required for required fields,
        but not for required=False fields for CharFields
        """
        form = TextForm()
        self.assertEqual(form.fields["name"].widget.attrs, {})
        self.assertEqual(form.fields["university"].widget.attrs, {})
        ParsleyForm = parsleyfy(TextForm)
        form = ParsleyForm()
        self.assertEqual(form.fields["name"].widget.attrs, {"data-required": "true"})
        self.assertEqual(form.fields["university"].widget.attrs, {})


class CharFieldDecoratedTest(TestCase):
    def test_decorated(self):
        "Tests that parsleyfy works as a class Decorator"
        form = TextForm2()
        self.assertEqual(form.fields["name"].widget.attrs, {"data-required": "true"})
        self.assertEqual(form.fields["university"].widget.attrs, {})


class FieldTypeFormTest(TestCase):
    def test_fields(self):
        "Tests that parsleyfy adds data-required for things other than CharField"
        form = FieldTypeForm()
        fields = form.fields
        self.assertEqual(fields["url"].widget.attrs["data-required"], "true")
        self.assertFalse("data-required" in fields["url2"].widget.attrs)
        self.assertEqual(fields["email"].widget.attrs["data-required"], "true")
        self.assertFalse("data-required" in fields["email2"].widget.attrs)


class DataTypeTest(TestCase):
    def test_data_types(self):
        "Test that different field types get correct data-type"
        form = FieldTypeForm()
        fields = form.fields
        self.assertTrue("data-type" in fields["url"].widget.attrs)
        self.assertEqual(fields["url"].widget.attrs["data-type"], "url")
        self.assertTrue("data-type" in fields["email"].widget.attrs)
        self.assertEqual(fields["email"].widget.attrs["data-type"], "email")
        self.assertEqual(fields["age"].widget.attrs["data-type"], "digits")
        self.assertEqual(fields["income"].widget.attrs["data-type"], "number")
        self.assertEqual(fields["income2"].widget.attrs["data-type"], "number")
        self.assertEqual(fields["topnav"].widget.attrs["data-regexp"], "#[A-Fa-f0-9]{6}")
        self.assertNotIn("data-regexp-flag", fields["topnav"].widget.attrs)
        self.assertEqual(fields["topnav2"].widget.attrs["data-regexp"], "#[a-z]+")
        self.assertEqual(fields["topnav2"].widget.attrs["data-regexp-flag"], "i")


class LengthTest(TestCase):
    def test_length(self):
        form = FieldTypeForm()
        fields = form.fields
        name_attrs = fields["name"].widget.attrs
        self.assertTrue("data-minlength" in name_attrs)
        self.assertEqual(name_attrs["data-minlength"], 3)
        self.assertEqual(name_attrs["data-maxlength"], 30)


class ValueTest(TestCase):
    def test_value(self):
        form = FieldTypeForm()
        fields = form.fields
        num_attrs = fields['some_num'].widget.attrs
        self.assertTrue("data-min" in num_attrs, True)
        self.assertTrue("data-max" in num_attrs, True)
        self.assertEqual(num_attrs["data-min"], 10)
        self.assertEqual(num_attrs["data-max"], 100)


class FormWithWidgetsTest(TestCase):
    def test_widgets(self):
        "Assert that @parsleyfy doesn't cloober existing attrs"
        form = FormWithWidgets()
        self.assertTrue(form.fields["description"].widget, forms.TextInput)
        self.assertEqual("highlight", form.fields["blurb"].widget.attrs["class"])


class TestMetadata(TestCase):
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


class TestModelForm(TestCase):
    def test_model_form(self):
        form = StudentModelForm()
        fields = form.fields
        foo_attrs = fields["name"].widget.attrs
        self.assertEqual(foo_attrs["data-required"], "true")

    def test_model_form_save(self):
        form = StudentModelForm({"name": "Luke Skywalker"})
        form.save(commit=False)


class TestCustomInit(TestCase):
    def test_custom_init(self):
        form = FormWithCustomInit()
        self.assertEqual(form.fields["description"].initial, "Hello")

    def test_custom_choices(self):
        form = FormWithCustomChoices()
        self.assertNotEqual(len(form.fields['state'].choices), 0)
        self.assertEqual(form.fields['state'].choices,
                    [("NY", "NY"), ("OH", "OH")])


class TestCleanFields(TestCase):
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


class TestExtraAttributes(TestCase):
    def test_equalto(self):
        form = ExtraDataForm()
        attrs = form.fields["email2"].widget.attrs
        self.assertEqual(attrs, {
            "data-type": "email",
            "data-required": "true",
            "data-equalto-message": "Must match",
            "data-equalto": "#id_email",
        })

    def test_default_data(self):
        form = ExtraDataForm()
        attrs = form.fields["name"].widget.attrs
        self.assertEqual(attrs, {
            "data-required": "true",
            "data-error-message": "Name invalid",
        })

    def test_boolean_values(self):
        form = ExtraDataForm()
        attrs = form.fields["hide_errors"].widget.attrs
        self.assertEqual(attrs, {
            "data-required": "true",
            "data-show-errors": "false",
        })

    def test_missing_field(self):
        ExtraDataMissingFieldForm()  # No error should be raised


class TestAdminMixin(TestCase):
    def test_media(self):
        student_admin = StudentAdmin(Student, admin.site)
        js = student_admin.media.render_js()
        self.assertIn(
            '<script type="text/javascript" src="/static/parsley/js/parsley-standalone.min.js"></script>',
            js
        )
        self.assertIn(
            '<script type="text/javascript" src="/static/parsley/js/parsley.django-admin.js"></script>',
            js
        )


class TestFormMedia(TestCase):

    def test_form_media(self):
        form = FormWithoutMedia()
        js = form.media.render_js()
        self.assertIn(
            '<script type="text/javascript" src="/static/parsley/js/parsley-standalone.min.js"></script>',
            js
        )

    def test_existing_form_media(self):
        form = FormWithMedia()
        js = form.media.render_js()
        self.assertIn(
            '<script type="text/javascript" src="/static/jquery.min.js"></script>',
            js
        )
        self.assertIn(
            '<script type="text/javascript" src="/static/parsley/js/parsley-standalone.min.js"></script>',
            js
        )


class TestMultiValueField(TestCase):
    def test_parsley_attributes(self):
        form = MultiWidgetForm()
        fields = form.fields["ssn"].fields
        self.assertEqual(fields[0].widget.attrs, {
            "data-minlength": 3,
            "data-maxlength": 3,
            "maxlength": "3",
            "data-regexp": r'^(\d)+$',
        })
        self.assertEqual(fields[1].widget.attrs, {
            "data-minlength": 3,
            "data-maxlength": 3,
            "maxlength": "3",
            "data-regexp": r'^(\d)+$',
        })
        self.assertEqual(fields[2].widget.attrs, {
            "data-minlength": 4,
            "data-maxlength": 4,
            "maxlength": "4",
            "data-regexp": r'^(\d)+$',
        })
