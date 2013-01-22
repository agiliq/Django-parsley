from django import forms

def parsleyfy(klass):
    class ParsleyClass(klass):
        def __init__(self, *args, **kwargs):
            super(ParsleyClass, self).__init__(*args, **kwargs)
            for key, val in self.fields.items():
                if val.required:
                    val.widget.attrs.update({"data-required": "true"})
                if type(val) == forms.URLField:
                    val.widget.attrs.update({"data-type": "url"})
                if type(val) == forms.EmailField:
                    val.widget.attrs.update({"data-type": "email"})

    return ParsleyClass
