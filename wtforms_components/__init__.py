from wtforms import Form
from .fields import (
    ColorField,
    DateField,
    DateTimeField,
    DateTimeLocalField,
    DecimalField,
    DecimalSliderField,
    EmailField,
    IntegerField,
    IntegerSliderField,
    NumberRangeField,
    PassiveHiddenField,
    PhoneNumberField,
    SearchField,
    SelectField,
    SelectMultipleField,
    TimeField,
)
from .validators import DateRange, Unique, If, Chain, Email, TimeRange
from .widgets import ReadOnlyWidgetProxy, NumberInput, SelectWidget


__all__ = (
    Chain,
    ColorField,
    DateField,
    DateRange,
    DateTimeField,
    DateTimeLocalField,
    DecimalField,
    DecimalSliderField,
    Email,
    EmailField,
    If,
    IntegerField,
    IntegerSliderField,
    NumberInput,
    NumberRangeField,
    PassiveHiddenField,
    PhoneNumberField,
    SearchField,
    SelectField,
    SelectMultipleField,
    SelectWidget,
    TimeField,
    TimeRange,
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
