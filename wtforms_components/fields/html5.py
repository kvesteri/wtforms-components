from wtforms.fields import html5
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


class IntegerField(html5.IntegerField):
    widget = NumberInput(step='1')


class DecimalField(html5.DecimalField):
    widget = NumberInput(step='any')


class DateTimeLocalField(html5.DateTimeField):
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


class DateTimeField(html5.DateTimeField):
    widget = DateTimeInput()


class DateField(html5.DateField):
    widget = DateInput()


class IntegerSliderField(html5.IntegerRangeField):
    widget = RangeInput(step='1')


class DecimalSliderField(html5.DecimalRangeField):
    widget = RangeInput(step='any')


class SearchField(html5.SearchField):
    widget = SearchInput()


class StringField(_StringField):
    widget = TextInput()
