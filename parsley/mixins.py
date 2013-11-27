from parsley.decorators import parsleyfy


class ParsleyAdminMixin(object):

    def get_form(self, *args, **kwargs):
        form = super(ParsleyAdminMixin, self).get_form(*args, **kwargs)
        return parsleyfy(form)

    class Media:
        js = (
            "//code.jquery.com/jquery-1.10.1.min.js",
            "parsley/js/parsley.min.js",
            "parsley/js/parsley.django-admin.js",
        )
