class ParsleyChoiceFieldRendererMixin(object):
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield self[i]

    def __getitem__(self, idx):
        choice = self.choices[idx]
        if idx == len(self.choices) - 1:
            self.attrs["{prefix}-required".format(prefix=self.parsley_namespace)] = "true"
        return super(ParsleyChoiceFieldRendererMixin, self).__getitem__(idx)
