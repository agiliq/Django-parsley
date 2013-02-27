from django import forms


def parsleyfy(klass):
    "A decorator to add data-* attributes to your form.fields"
    old_init = klass.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        for key, val in self.fields.items():
            if val.required:
                val.widget.attrs.update({"data-required": "true"})
            if isinstance(val, forms.URLField):
                val.widget.attrs.update({"data-type": "url"})
            if isinstance(val, forms.EmailField):
                val.widget.attrs.update({"data-type": "email"})
            if isinstance(val, forms.IntegerField):
                val.widget.attrs.update({"data-type": "digits"})
            if isinstance(val, forms.DecimalField):
                val.widget.attrs.update({"data-type": "number"})
            if isinstance(val, forms.RegexField):
                val.widget.attrs.update({"data-regexp": val.regex.pattern})
            if hasattr(val, "max_length") and val.max_length:
                val.widget.attrs.update({"data-maxlength": val.max_length})
            if hasattr(val, "min_length") and val.min_length:
                val.widget.attrs.update({"data-minlength": val.min_length})
            if hasattr(val, 'min_value') and val.min_value:
                val.widget.attrs.update({'data-min': val.min_value})
            if hasattr(val, 'max_value') and val.max_value:
                val.widget.attrs.update({'data-max': val.max_value})
    klass.__init__ = new_init

    return klass
