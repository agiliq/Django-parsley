import re

from django import forms


def update_widget_attrs(field):
    attrs = field.widget.attrs
    if field.required:
        attrs["data-required"] = "true"
    if isinstance(field, forms.URLField):
        attrs["data-type"] = "url"
    if isinstance(field, forms.EmailField):
        attrs["data-type"] = "email"
    if isinstance(field, forms.IntegerField):
        attrs["data-type"] = "digits"
    if isinstance(field, forms.DecimalField):
        attrs["data-type"] = "number"
    if isinstance(field, forms.FloatField):
        attrs["data-type"] = "number"
    if isinstance(field, forms.RegexField):
        attrs.update({"data-regexp": field.regex.pattern})
        if field.regex.flags & re.IGNORECASE:
            attrs.update({"data-regexp-flag": "i"})
    if isinstance(field, forms.MultiValueField):
        for subfield in field.fields:
            update_widget_attrs(subfield)
    if hasattr(field, "max_length") and field.max_length:
        attrs["data-maxlength"] = field.max_length
    if hasattr(field, "min_length") and field.min_length:
        attrs["data-minlength"] = field.min_length
    if hasattr(field, 'min_value') and field.min_value:
        attrs['data-min'] = field.min_value
    if hasattr(field, 'max_value') and field.max_value:
        attrs['data-max'] = field.max_value


def parsleyfy(klass):
    "A decorator to add data-* attributes to your form.fields"
    old_init = klass.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        for _, field in self.fields.items():
            update_widget_attrs(field)
        extras = getattr(getattr(self, 'Meta', None), 'parsley_extras', {})
        for field_name, data in extras.items():
            for key, value in data.items():
                attrs = self.fields[field_name].widget.attrs
                if key == 'equalto':
                    # Use HTML id for data-equalto
                    attrs['data-equalto'] = '#' + self[value].id_for_label
                else:
                    attrs['data-%s' % key] = value
    klass.__init__ = new_init

    try:
        klass.Media.js += ("parsley/js/parsley-standalone.min.js",)
    except AttributeError:
        class Media:
            js = (
                "parsley/js/parsley-standalone.min.js",
            )
        klass.Media = Media

    return klass
