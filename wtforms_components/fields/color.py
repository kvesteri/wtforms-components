from ..widgets import ColorInput
from .html5 import StringField


class ColorField(StringField):
    """
    A string field representing a Color object from python colour package.

    .. _colours:
       https://github.com/vaab/colour

    Represents an ``<input type="color">``.
    """
    widget = ColorInput()

    error_msg = u'Not a valid color.'

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data:
            return str(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        from colour import Color

        if valuelist:
            if valuelist[0] == u'' or valuelist[0] == '':
                self.data = None
            else:
                try:
                    self.data = Color(valuelist[0])
                except AttributeError:
                    self.data = None
                    raise ValueError(self.gettext(self.error_msg))
