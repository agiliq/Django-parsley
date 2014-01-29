from parsley.decorators import parsleyfy


class ParsleyAdminMixin(object):

    def get_form(self, *args, **kwargs):
        form = super(ParsleyAdminMixin, self).get_form(*args, **kwargs)
        return parsleyfy(form)
