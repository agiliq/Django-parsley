class ParsleyChoiceFieldRendererMixin(object):
    def __init__(self, name, value, attrs, choices):
        self.name = name
        self.value = value
        self.attrs = attrs
        self._choices = choices

    @property
    def choices(self):
        def choices_iter():
            choices_list = self._choices
            for idx, choice in enumerate(choices_list):
                if idx == len(choices_list) - 1:
                    self.attrs["{prefix}-required".format(prefix=self.parsley_namespace)] = "true"
                yield choice
        return choices_iter()
