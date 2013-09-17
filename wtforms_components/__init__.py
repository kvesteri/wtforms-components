from wtforms import Form
from .fields import (
    ColorField,
    DateField,
    DateTimeField,
    DateTimeLocalField,
    DecimalField,
    DecimalSliderField,
    EmailField,
    GroupedQuerySelectField,
    IntegerField,
    IntegerSliderField,
    NumberRangeField,
    PassiveHiddenField,
    PhoneNumberField,
    SearchField,
    SelectField,
    SelectMultipleField,
    SplitDateTimeField,
    StringField,
    TimeField,
)
from .validators import DateRange, Unique, If, Chain, Email, TimeRange
from .widgets import ReadOnlyWidgetProxy, NumberInput, SelectWidget


__version__ = '0.7.1'


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
    GroupedQuerySelectField,
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
    SplitDateTimeField,
    StringField,
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
