from __future__ import absolute_import
import time
import datetime
from wtforms.fields import Field
from ..widgets import TimeInput


class TimeField(Field):
    """
    A text field which stores a `datetime.time` matching a format.
    """
    widget = TimeInput()
    error_msg = 'Not a valid time.'

    def __init__(self, label=None, validators=None, format='%H:%M', **kwargs):
        super(TimeField, self).__init__(label, validators, **kwargs)
        self.format = format

    def _value(self):
        if self.raw_data:
            return ' '.join(self.raw_data)
        else:
            return (
                self.data is not None and self.data.strftime(self.format)
                or ''
            )

    def process_formdata(self, valuelist):
        if valuelist:
            time_str = ' '.join(valuelist)
            try:
                self.data = datetime.time(
                    *time.strptime(time_str, self.format)[3:5]
                )
            except ValueError:
                self.data = None
                raise ValueError(self.gettext(self.error_msg))
