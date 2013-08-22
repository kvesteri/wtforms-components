from sqlalchemy_utils import NumberRange, NumberRangeException
from .html5 import StringField


class NumberRangeField(StringField):
    """
    A string field representing a NumberRange object from
    `SQLAlchemy-Utils`_.

    .. _SQLAlchemy-Utils:
       https://github.com/kvesteri/sqlalchemy-utils
    """
    error_msg = u'Not a valid number range value'

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data:
            return str(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == u'' or valuelist[0] == '':
                self.data = None
            else:
                try:
                    self.data = NumberRange.from_str(valuelist[0])
                except NumberRangeException:
                    self.data = None
                    raise ValueError(self.gettext(self.error_msg))
