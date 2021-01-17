try:
    from wtforms.fields.html5 import (
        DateField,
        DateTimeField,
        DecimalField,
        DecimalRangeField,
        IntegerField,
        IntegerRangeField,
        SearchField
    )
except ImportError:  # wtforms>=3
    from wtforms.fields import (
        DateField,
        DateTimeField,
        DecimalField,
        DecimalRangeField,
        IntegerField,
        IntegerRangeField,
        SearchField
    )
from wtforms.fields import StringField as _StringField

from ..widgets import (
    DateInput,
    DateTimeInput,
    DateTimeLocalInput,
    EmailInput,
    NumberInput,
    RangeInput,
    SearchInput,
    TextInput
)


class EmailField(_StringField):
    widget = EmailInput()


class IntegerField(IntegerField):
    widget = NumberInput(step='1')


class DecimalField(DecimalField):
    widget = NumberInput(step='any')


class DateTimeLocalField(DateTimeField):
    def __init__(
        self,
        label=None,
        validators=None,
        format='%Y-%m-%dT%H:%M:%S',
        **kwargs
    ):
        super(DateTimeLocalField, self).__init__(
            label,
            validators,
            format,
            **kwargs
        )
    widget = DateTimeLocalInput()


class DateTimeField(DateTimeField):
    widget = DateTimeInput()


class DateField(DateField):
    widget = DateInput()


class IntegerSliderField(IntegerRangeField):
    widget = RangeInput(step='1')


class DecimalSliderField(DecimalRangeField):
    widget = RangeInput(step='any')


class SearchField(SearchField):
    widget = SearchInput()


class StringField(_StringField):
    widget = TextInput()
