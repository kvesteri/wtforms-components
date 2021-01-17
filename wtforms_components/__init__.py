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
    IntegerField,
    IntegerSliderField,
    IntIntervalField,
    JSONField,
    PassiveHiddenField,
    SearchField,
    SelectField,
    SelectMultipleField,
    SplitDateTimeField,
    StringField,
    TimeField
)
from .validators import Chain, DateRange, Email, If, TimeRange
from .widgets import NumberInput, ReadOnlyWidgetProxy, SelectWidget

__version__ = '0.10.5'


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
    If,
    IntegerField,
    IntegerSliderField,
    IntIntervalField,
    JSONField,
    NumberInput,
    PassiveHiddenField,
    SearchField,
    SelectField,
    SelectMultipleField,
    SelectWidget,
    SplitDateTimeField,
    StringField,
    TimeField,
    TimeRange
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


def do_nothing(*args, **kwargs):
    pass


def read_only(field):
    field.widget = ReadOnlyWidgetProxy(field.widget)
    field.process = do_nothing
    field.populate_obj = do_nothing
    return field
