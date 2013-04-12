from wtforms import Form
from .fields import (
    NumberRangeField,
    PassiveHiddenField,
    SelectField,
    SelectMultipleField,
    PhoneNumberField
)
from .validators import DateRange, Unique, If, Chain, Email


__all__ = (
    Chain,
    DateRange,
    Email,
    If,
    NumberRangeField,
    PassiveHiddenField,
    PhoneNumberField,
    SelectField,
    SelectMultipleField,
    Unique,
)


class ModelForm(Form):
    """
    Simple ModelForm, use this if your form needs to use the Unique validator
    """
    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        Form.__init__(
            self, formdata=formdata, obj=obj, prefix=prefix, **kwargs
        )
        self._obj = obj
