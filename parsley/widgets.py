class ParsleyChoiceFieldRendererMixin(object):
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield self[i]

    def __getitem__(self, idx):
        choice = self.choices[idx] 
        attrs = self.attrs.copy()
        if idx == len(self.choices) - 1:
            attrs["{prefix}-mincheck".format(prefix=self.parsley_namespace)] = "1"
        return self.choice_input_class(self.name, self.value, attrs, choice, idx)
