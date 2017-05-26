import re
import six

from django import forms
from django.template import Context, Template
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from parsley.decorators import parsleyfy, parsley_form

from .forms import (TextForm, TextForm2, FieldTypeForm, ExtraDataForm,
        ExtraDataMissingFieldForm, FormWithWidgets, StudentModelForm,
        FormWithCleanField, FormWithCustomInit, FormWithCustomChoices,
        MultiWidgetForm, CustomErrorMessageForm,
        CustomPrefixForm, FormWithRadioSelect, FormWithRadioSelectNotRequired)


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
        Tests that parsleyfy will add data-parsley-required for required fields,
        but not for required=False fields for CharFields
        """
        form = TextForm()
        self.assertEqual(form.fields["name"].widget.attrs, {})
        self.assertEqual(form.fields["university"].widget.attrs, {})
        form = parsley_form(TextForm())
        self.assertAttrsEqual(form.fields["name"].widget.attrs, {
            "data-parsley-required": "true",
            "data-parsley-required-message": _("This field is required.")
        })
        self.assertEqual(form.fields["university"].widget.attrs, {})


class CharFieldDecoratedTest(ParsleyTestCase):
    def test_decorated(self):
        "Tests that parsleyfy works as a class Decorator"
        form = TextForm2()
        self.assertAttrsEqual(form.fields["name"].widget.attrs, {
            "data-parsley-required": "true",
            "data-parsley-required-message": _("This field is required.")
        })
        self.assertEqual(form.fields["university"].widget.attrs, {})


class FieldTypeFormTest(ParsleyTestCase):
    def test_fields(self):
        "Tests that parsleyfy adds data-parsley-required for things other than CharField"
        form = FieldTypeForm()
        fields = form.fields
        self.assertEqual(fields["url"].widget.attrs["data-parsley-required"], "true")
        self.assertFalse("data-parsley-required" in fields["url2"].widget.attrs)
        self.assertEqual(fields["email"].widget.attrs["data-parsley-required"], "true")
        self.assertFalse("data-parsley-required" in fields["email2"].widget.attrs)


class DataTypeTest(ParsleyTestCase):
    def test_data_types(self):
        "Test that different field types get correct data-parsley-type"
        form = FieldTypeForm()
        fields = form.fields
        self.assertTrue("data-parsley-type" in fields["url"].widget.attrs)
        self.assertEqual(fields["url"].widget.attrs["data-parsley-type"], "url")
        self.assertTrue("data-parsley-type" in fields["email"].widget.attrs)
        self.assertEqual(fields["email"].widget.attrs["data-parsley-type"], "email")
        self.assertEqual(fields["age"].widget.attrs["data-parsley-type"], "digits")
        self.assertEqual(fields["income"].widget.attrs["data-parsley-type"], "number")
        self.assertEqual(fields["income2"].widget.attrs["data-parsley-type"], "number")
        self.assertEqual(fields["topnav"].widget.attrs["data-parsley-pattern"], "#[A-Fa-f0-9]{6}")
        self.assertNotIn("data-parsley-regexp-flag", fields["topnav"].widget.attrs)
        self.assertEqual(fields["topnav2"].widget.attrs["data-parsley-pattern"], "#[a-z]+")
        self.assertEqual(fields["topnav2"].widget.attrs["data-parsley-regexp-flag"], "i")


class LengthTest(ParsleyTestCase):
    def test_length(self):
        form = FieldTypeForm()
        fields = form.fields
        name_attrs = fields["name"].widget.attrs
        self.assertTrue("data-parsley-minlength" in name_attrs)
        self.assertEqual(name_attrs["data-parsley-minlength"], 3)
        self.assertEqual(name_attrs["data-parsley-maxlength"], 30)
        self.assertEqual(fields["amount"].widget.attrs["data-parsley-max"], 999999999999.99)
        self.assertEqual(fields["amount"].widget.attrs["data-parsley-min"], -999999999999.99)

class ValueTest(ParsleyTestCase):
    def test_value(self):
        form = FieldTypeForm()
        fields = form.fields
        num_attrs = fields['some_num'].widget.attrs
        self.assertTrue("data-parsley-min" in num_attrs, True)
        self.assertTrue("data-parsley-max" in num_attrs, True)
        self.assertEqual(num_attrs["data-parsley-min"], 10)
        self.assertEqual(num_attrs["data-parsley-max"], 100)


class FormWithWidgetsTest(ParsleyTestCase):
    def test_widgets(self):
        "Assert that @parsleyfy doesn't cloober existing attrs"
        form = FormWithWidgets()
        self.assertTrue(form.fields["description"].widget, forms.TextInput)
        self.assertEqual("highlight", form.fields["blurb"].widget.attrs["class"])


class TestMetadata(ParsleyTestCase):
    def test_docstring(self):
        form1 = TextForm()
        form2 = parsley_form(TextForm())
        self.assertEqual(form1.__doc__, form2.__doc__)

    def test_module(self):
        form1 = TextForm()
        form2 = parsley_form(TextForm())
        self.assertEqual(form1.__module__, form2.__module__)

    def test_name(self):
        form1 = TextForm()
        form2 = parsley_form(TextForm())
        self.assertEqual(form1.__class__.__name__, form2.__class__.__name__)


class TestModelForm(ParsleyTestCase):
    def test_model_form(self):
        form = StudentModelForm()
        fields = form.fields
        foo_attrs = fields["name"].widget.attrs
        self.assertEqual(foo_attrs["data-parsley-required"], "true")

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


class TestRadioSelect(ParsleyTestCase):
    def test_radio_select(self):
        form = FormWithRadioSelect()
        self.assertEqual(form.fields['state'].choices,
                    [("NY", "NY"), ("OH", "OH")])
        radio_select_html = form.fields['state'].widget.render("state", "NY")
        self.assertEqual(1, len(re.findall('data-parsley-required', radio_select_html)))

    def test_radio_select_not_required(self):
        form = FormWithRadioSelectNotRequired()
        self.assertEqual(form.fields['state'].choices,
                    [("NY", "NY"), ("OH", "OH")])
        radio_select_html = form.fields['state'].widget.render("state", "NY")
        self.assertEqual(0, len(re.findall('data-parsley-required', radio_select_html)))


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
            "data-parsley-type": "email",
            "data-parsley-required": "true",
            "data-parsley-equalto-message": "Must match",
            "data-parsley-equalto": "#id_email",
            "data-parsley-required-message": _("This field is required."),
        })

    def test_default_data(self):
        form = ExtraDataForm()
        attrs = form.fields["name"].widget.attrs
        self.assertAttrsEqual(attrs, {
            "data-parsley-required": "true",
            "data-parsley-error-message": "Name invalid",
            "data-parsley-required-message": _("This field is required.")
        })

    def test_boolean_values(self):
        form = ExtraDataForm()
        attrs = form.fields["hide_errors"].widget.attrs
        self.assertAttrsEqual(attrs, {
            "data-parsley-required": "true",
            "data-parsley-show-errors": "false",
            "data-parsley-required-message": _("This field is required.")
        })

    def test_missing_field(self):
        ExtraDataMissingFieldForm()  # No error should be raised


class TestMultiValueField(ParsleyTestCase):
    def test_parsley_attributes(self):
        form = MultiWidgetForm()
        fields = form.fields["ssn"].fields
        self.assertAttrsEqual(fields[0].widget.attrs, {
            "data-parsley-minlength": 3,
            "data-parsley-maxlength": 3,
            "maxlength": "3",
            "data-parsley-pattern": r'^(\d)+$',
        })
        self.assertAttrsEqual(fields[1].widget.attrs, {
            "data-parsley-minlength": 3,
            "data-parsley-maxlength": 3,
            "maxlength": "3",
            "data-parsley-pattern": r'^(\d)+$',
        })
        self.assertAttrsEqual(fields[2].widget.attrs, {
            "data-parsley-minlength": 4,
            "data-parsley-maxlength": 4,
            "maxlength": "4",
            "data-parsley-pattern": r'^(\d)+$',
        })


class TestCustomErrorMessages(TestCase):

    def test_new_message(self):
        form = CustomErrorMessageForm()
        attrs = form.fields['name'].widget.attrs
        self.assertEqual(attrs, {
            "maxlength": '30',
            "data-parsley-maxlength": 30,
            "data-parsley-maxlength-message": "Please only 30 characters"
        })

    def test_field_type_message(self):
        form = CustomErrorMessageForm()
        attrs = form.fields['email'].widget.attrs
        self.assertEqual(attrs, {
            "data-parsley-type": "email",
            "data-parsley-type-message": "Invalid email"
        })

    def test_override_default_message(self):
        form = CustomErrorMessageForm()
        attrs = form.fields['favorite_color'].widget.attrs
        self.assertEqual(attrs, {
            "data-parsley-required": "true",
            "data-parsley-required-message": "Favorite color is required"
        })


class TestCustomPrefix(TestCase):

    def test_default_prefix(self):
        form = TextForm2()
        attrs = form.fields['name'].widget.attrs
        self.assertTrue('data-parsley-required' in attrs)

    def test_custom_prefix(self):
        form = CustomPrefixForm()
        attrs = form.fields['name'].widget.attrs
        self.assertTrue('custom-required' in attrs)


class TemplateTagTest(ParsleyTestCase):
    def test_basic(self):
        """
        Tests that parsleyfy will work using the template tag
        """

        template = Template("{% load parsley %}")
        form = TextForm()
        context = Context({'form': form})
        template.render(context)

        self.assertEqual(context['form'].fields["name"].widget.attrs, {})
        self.assertEqual(context['form'].fields["university"].widget.attrs, {})

        template = Template("{% load parsley %}{% parsleyfy form as form %}")
        form = TextForm()
        context = Context({'form': form})
        template.render(context)

        self.assertAttrsEqual(context['form'].fields["name"].widget.attrs, {
            "data-parsley-required": "true",
            "data-parsley-required-message": _("This field is required.")
        })
        self.assertEqual(context['form'].fields["university"].widget.attrs, {})