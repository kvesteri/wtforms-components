from wtforms import Form
from .fields import (
    ColorField,
    DateField,
    DateIntervalField,
    DateTimeField,
    DateTimeIntervalField,
    DateTimeLocalField,
    DecimalField,
    DecimalIntervalField,
    DecimalSliderField,
    EmailField,
    FloatIntervalField,
    GroupedQuerySelectField,
    IntegerField,
    IntegerSliderField,
    IntIntervalField,
    PassiveHiddenField,
    PhoneNumberField,
    SearchField,
    SelectField,
    SelectMultipleField,
    SplitDateTimeField,
    StringField,
    TimeField,
    WeekDaysField
)
from .validators import DateRange, Unique, If, Chain, Email, TimeRange
from .widgets import ReadOnlyWidgetProxy, NumberInput, SelectWidget


__version__ = '0.9.7'


__all__ = (
    Chain,
    ColorField,
    DateField,
    DateIntervalField,
    DateRange,
    DateTimeField,
    DateTimeIntervalField,
    DateTimeLocalField,
    DecimalField,
    DecimalIntervalField,
    DecimalSliderField,
    Email,
    EmailField,
    FloatIntervalField,
    GroupedQuerySelectField,
    If,
    IntegerField,
    IntegerSliderField,
    IntIntervalField,
    NumberInput,
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
    WeekDaysField
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
