from django.test import TestCase
from django import forms

from .forms import TextForm, TextForm2, FieldTypeForm, FormWithWidgets
from .decorators import parsleyfy

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
        self.assertEqual(fields["topnav"].widget.attrs["data-regexp"], "#[A-Fa-f0-9]{6}")

class LengthTest(TestCase):
    def test_length(self):
        form = FieldTypeForm()
        fields = form.fields
        name_attrs = fields["name"].widget.attrs
        self.assertTrue("data-minlength" in name_attrs)
        self.assertEqual(name_attrs["data-minlength"], 3)
        self.assertEqual(name_attrs["data-maxlength"], 30)


class FormWithWidgetsTest(TestCase):
    def test_widgets(self):
        "Assert that @parsleyfy doesn't cloober existing attrs"
        form = FormWithWidgets()
        self.assertTrue(form.fields["description"].widget, forms.TextInput)
        self.assertEqual("highlight", form.fields["blurb"].widget.attrs["class"])










