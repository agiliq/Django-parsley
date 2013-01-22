def parsleyfy(klass):
    class ParsleyClass(klass):
        def __init__(self, *args, **kwargs):
            super(ParsleyClass, self).__init__(*args, **kwargs)
            for key, val in self.fields.items():
                if val.required:
                    val.widget.attrs.update({"data-required": "true"})
    return ParsleyClass
