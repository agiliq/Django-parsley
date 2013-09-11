from django import forms


def parsleyfy(klass):
    "A decorator to add data-* attributes to your form.fields"
    old_init = klass.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        for _, field in self.fields.items():
            if field.required:
                field.widget.attrs.update({"data-required": "true"})
            if isinstance(field, forms.URLField):
                field.widget.attrs.update({"data-type": "url"})
            if isinstance(field, forms.EmailField):
                field.widget.attrs.update({"data-type": "email"})
            if isinstance(field, forms.IntegerField):
                field.widget.attrs.update({"data-type": "digits"})
            if isinstance(field, forms.DecimalField):
                field.widget.attrs.update({"data-type": "number"})
            if isinstance(field, forms.FloatField):
                field.widget.attrs.update({"data-type": "number"})
            if isinstance(field, forms.RegexField):
                field.widget.attrs.update({"data-regexp": field.regex.pattern})
            if hasattr(field, "max_length") and field.max_length:
                field.widget.attrs.update({"data-maxlength": field.max_length})
            if hasattr(field, "min_length") and field.min_length:
                field.widget.attrs.update({"data-minlength": field.min_length})
            if hasattr(field, 'min_value') and field.min_value:
                field.widget.attrs.update({'data-min': field.min_value})
            if hasattr(field, 'max_value') and field.max_value:
                field.widget.attrs.update({'data-max': field.max_value})
    klass.__init__ = new_init

    return klass
