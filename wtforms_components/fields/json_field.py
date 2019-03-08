from wtforms.fields import StringField
from wtforms import widgets
import json


class JSONField(StringField):
    """
    A text field which stores a `json`.
    """
    widget = widgets.TextArea()

    def __init__(self, label=None, validators=None, **kwargs):
        super(JSONField, self).__init__(label, validators, **kwargs)

    def _value(self):
        return json.dumps(self.data) if self.data else ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = json.loads(valuelist[0])
            except ValueError:
                self.data = None
                raise ValueError('This field contains invalid JSON')
        else:
            self.data = None

    def pre_validate(self, form):
        if self.data:
            try:
                json.dumps(self.data)
            except TypeError:
                self.data = None
                raise ValueError('This field contains invalid JSON')
