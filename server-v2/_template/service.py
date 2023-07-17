class TemplateService():
    def __init__(self):
        self._field = []

    @property
    def field(self):
        return self._field