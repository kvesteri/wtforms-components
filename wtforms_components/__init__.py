from wtforms import Form
from .fields import (
    ColorField,
    DateField,
    DateTimeField,
    DateTimeLocalField,
    DecimalField,
    IntegerField,
    NumberRangeField,
    PassiveHiddenField,
    PhoneNumberField,
    SelectField,
    SelectMultipleField,
    TimeField,
)
from .validators import DateRange, Unique, If, Chain, Email
from .widgets import ReadOnlyWidgetProxy, NumberInput, SelectWidget


__all__ = (
    Chain,
    ColorField,
    DateRange,
    DateField,
    DateTimeField,
    DateTimeLocalField,
    DecimalField,
    Email,
    If,
    IntegerField,
    NumberInput,
    NumberRangeField,
    PassiveHiddenField,
    PhoneNumberField,
    SelectField,
    SelectMultipleField,
    SelectWidget,
    TimeField,
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


def read_only(field):
    field.widget = ReadOnlyWidgetProxy(field.widget)
    return field
