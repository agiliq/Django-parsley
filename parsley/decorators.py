import re
import types

from django import forms
from parsley.widgets import ParsleyChoiceFieldRendererMixin

FIELD_TYPES = [
    (forms.URLField, "url"),
    (forms.EmailField, "email"),
    (forms.IntegerField, "digits"),
    (forms.DecimalField, "number"),
    (forms.FloatField, "number"),
]


FIELD_ATTRS = [
    ("min_length", "minlength"),
    ("max_length", "maxlength"),
    ("min_value", "min"),
    ("max_value", "max"),
]


def update_widget_attrs(field, prefix='data'):
    attrs = field.widget.attrs
    if field.required:
        if isinstance(field.widget, forms.widgets.RadioSelect):
            try:
                # django >= 1.11
                original_create_option = field.widget.create_option

                def new_create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
                    if index == len(self.choices) - 1:
                        attrs = attrs or {}
                        attrs["{prefix}-required".format(prefix=prefix)] = "true"

                    return original_create_option(name, value, label, selected, index, subindex, attrs)

                field.widget.create_option = types.MethodType(new_create_option, field.widget)
            except AttributeError:
                # django < 1.11

                # Use a mixin, to try and support non-standard renderers if possible
                class ParsleyChoiceFieldRenderer(ParsleyChoiceFieldRendererMixin, field.widget.renderer):
                    parsley_namespace = prefix
                field.widget.renderer = ParsleyChoiceFieldRenderer
        else:
            attrs["{prefix}-required".format(prefix=prefix)] = "true"
            error_message = field.error_messages.get('required', None)
            if error_message:
                attrs["{prefix}-required-message".format(prefix=prefix)] = error_message

    if isinstance(field, forms.RegexField):
        attrs.update({"{prefix}-pattern".format(prefix=prefix): field.regex.pattern})

        error_message = field.error_messages.get('invalid', None)
        if error_message:
            attrs["{prefix}-pattern-message".format(prefix=prefix)] = error_message

        if field.regex.flags & re.IGNORECASE:
            attrs.update({"{prefix}-regexp-flag".format(prefix=prefix): "i"})

    if isinstance(field, forms.MultiValueField):
        for subfield in field.fields:
            update_widget_attrs(subfield)

    # Set {prefix}-* attributes for parsley based on Django field attributes
    for attr, data_attr, in FIELD_ATTRS:
        if getattr(field, attr, None):
            attrs["{prefix}-{0}".format(data_attr, prefix=prefix)] = getattr(field, attr)

            error_message = field.error_messages.get(attr, None)
            if error_message:
                attrs["{prefix}-{0}-message".format(data_attr, prefix=prefix)] = error_message

    # Set {prefix}-type attribute based on Django field instance type
    for klass, field_type in FIELD_TYPES:
        if isinstance(field, klass):
            attrs["{prefix}-type".format(prefix=prefix)] = field_type

            error_message = field.error_messages.get('invalid', None)
            if error_message:
                attrs["{prefix}-type-message".format(field_type, prefix=prefix)] = error_message

def parsley_form(form):
    prefix = getattr(getattr(form, 'Meta', None), 'parsley_namespace', 'data-parsley')
    for _, field in form.fields.items():
        update_widget_attrs(field, prefix)
    extras = getattr(getattr(form, 'Meta', None), 'parsley_extras', {})
    for field_name, data in extras.items():
        for key, value in data.items():
            if field_name not in form.fields:
                continue
            attrs = form.fields[field_name].widget.attrs
            if key == 'equalto':
                # Use HTML id for {prefix}-equalto
                value = '#' + form[value].id_for_label
            if isinstance(value, bool):
                value = "true" if value else "false"
            attrs["{prefix}-%s".format(prefix=prefix) % key] = value
    return form

def parsleyfy(klass):
    "A decorator to add {prefix}-* attributes to your form.fields"
    old_init = klass.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        parsley_form(self)

    klass.__init__ = new_init

    return klass
