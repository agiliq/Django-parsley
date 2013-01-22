from django.test import TestCase

from .forms import TextForm
from .decorators import parsleyfy

class CharFieldTest(TestCase):
    def test_basic(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        form = TextForm()
        self.assertEqual(form.fields["name"].widget.attrs, {})
        ParsleyForm = parsleyfy(TextForm)
        form = ParsleyForm()
        self.assertEqual(form.fields["name"].widget.attrs, {"data-required": "true"})


