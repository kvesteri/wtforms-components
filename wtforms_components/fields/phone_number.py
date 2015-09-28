from sqlalchemy_utils import PhoneNumber

from ..widgets import TelInput
from .html5 import StringField


class PhoneNumberField(StringField):
    """
    A string field representing a PhoneNumber object from
    `SQLAlchemy-Utils`_.

    .. _SQLAlchemy-Utils:
       https://github.com/kvesteri/sqlalchemy-utils

    :param country_code:
        Country code of the phone number.
    :param display_format:
        The format in which the phone number is displayed.
    """
    widget = TelInput()
    error_msg = u'Not a valid phone number value'

    def __init__(self, label=None, validators=None, country_code='US',
                 display_format='national',
                 **kwargs):
        super(PhoneNumberField, self).__init__(label, validators, **kwargs)
        self.country_code = country_code
        self.display_format = display_format

    def _value(self):
        # self.data holds a PhoneNumber object, use it before falling back
        # to self.rawdata which holds a string
        if self.data:
            return getattr(self.data, self.display_format)
        elif self.raw_data:
            return self.raw_data[0]
        else:
            return u''

    def process_formdata(self, valuelist):
        import phonenumbers

        if valuelist:
            if valuelist[0] == u'':
                self.data = None
            else:
                try:
                    self.data = PhoneNumber(
                        valuelist[0],
                        self.country_code
                    )
                    if not self.data.is_valid_number():
                        self.data = None
                        raise ValueError(self.gettext(self.error_msg))
                except phonenumbers.phonenumberutil.NumberParseException:
                    self.data = None
                    raise ValueError(self.gettext(self.error_msg))
