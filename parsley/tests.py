from django.test import TestCase

from .forms import TextForm, TextForm2
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
        form = TextForm2()
        self.assertEqual(form.fields["name"].widget.attrs, {"data-required": "true"})
        self.assertEqual(form.fields["university"].widget.attrs, {})


