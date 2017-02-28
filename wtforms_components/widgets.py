from cgi import escape
from copy import copy

import six
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import Select as _Select
from wtforms.widgets import html_params, HTMLString, Input

from .validators import DateRange, TimeRange


def min_max(field, validator_class):
    """
    Returns maximum minimum and minimum maximum value for given validator class
    of given field.

    :param field: WTForms Field object
    :param validator_class: WTForms Validator class

    Example::


        class MyForm(Form):
            some_integer_field = IntegerField(
                validators=[Length(min=3, max=6), Length(min=4, max=7)]
            )

        form = MyForm()

        min_max(form.some_integer_field, Length)
        # {'min': 4, 'max': 6}
    """
    min_values = []
    max_values = []
    for validator in field.validators:
        if isinstance(validator, validator_class):
            if validator.min is not None:
                min_values.append(validator.min)
            if validator.max is not None:
                max_values.append(validator.max)

    data = {}
    if min_values:
        data['min'] = max(min_values)
    if max_values:
        data['max'] = min(max_values)
    return data


def has_validator(field, validator_class):
    """
    Returns whether or not given field has an instance of given validator class
    in the validators property.

    :param field: WTForms Field object
    :param validator_class: WTForms Validator class
    """
    return any([
        isinstance(validator, validator_class)
        for validator in field.validators
    ])


class HTML5Input(Input):
    def __init__(self, **kwargs):
        self.options = kwargs

    def __call__(self, field, **kwargs):
        if has_validator(field, DataRequired):
            kwargs.setdefault('required', True)

        for key, value in self.range_validators(field).items():
            kwargs.setdefault(key, value)

        if hasattr(field, 'widget_options'):
            for key, value in self.field.widget_options:
                kwargs.setdefault(key, value)

        options_copy = copy(self.options)
        options_copy.update(kwargs)
        return super(HTML5Input, self).__call__(field, **options_copy)

    def range_validators(self, field):
        return {}


class BaseDateTimeInput(HTML5Input):
    """
    Base class for TimeInput, DateTimeLocalInput, DateTimeInput and
    DateInput widgets
    """
    range_validator_class = DateRange

    def range_validators(self, field):
        data = min_max(field, self.range_validator_class)
        if 'min' in data:
            data['min'] = data['min'].strftime(self.format)
        if 'max' in data:
            data['max'] = data['max'].strftime(self.format)
        return data


class TextInput(HTML5Input):
    input_type = 'text'


class SearchInput(HTML5Input):
    """
    Renders an input with type "search".
    """
    input_type = 'search'


class MonthInput(HTML5Input):
    """
    Renders an input with type "month".
    """
    input_type = 'month'


class WeekInput(HTML5Input):
    """
    Renders an input with type "week".
    """
    input_type = 'week'


class RangeInput(HTML5Input):
    """
    Renders an input with type "range".
    """
    input_type = 'range'


class URLInput(HTML5Input):
    """
    Renders an input with type "url".
    """
    input_type = 'url'


class ColorInput(HTML5Input):
    """
    Renders an input with type "tel".
    """
    input_type = 'color'


class TelInput(HTML5Input):
    """
    Renders an input with type "tel".
    """
    input_type = 'tel'


class EmailInput(HTML5Input):
    """
    Renders an input with type "email".
    """
    input_type = 'email'


class TimeInput(BaseDateTimeInput):
    """
    Renders an input with type "time".

    Adds min and max html5 field parameters based on field's TimeRange
    validator.
    """
    input_type = 'time'
    range_validator_class = TimeRange
    format = '%H:%M:%S'


class DateTimeLocalInput(BaseDateTimeInput):
    """
    Renders an input with type "datetime-local".

    Adds min and max html5 field parameters based on field's DateRange
    validator.
    """
    input_type = 'datetime-local'
    format = '%Y-%m-%dT%H:%M:%S'


class DateTimeInput(BaseDateTimeInput):
    """
    Renders an input with type "datetime".

    Adds min and max html5 field parameters based on field's DateRange
    validator.
    """
    input_type = 'datetime'
    format = '%Y-%m-%dT%H:%M:%SZ'


class DateInput(BaseDateTimeInput):
    """
    Renders an input with type "date".

    Adds min and max html5 field parameters based on field's DateRange
    validator.
    """
    input_type = 'date'
    format = '%Y-%m-%d'


class NumberInput(HTML5Input):
    """
    Renders an input with type "number".

    Adds min and max html5 field parameters based on field's NumberRange
    validator.
    """
    input_type = 'number'
    range_validator_class = NumberRange

    def range_validators(self, field):
        return min_max(field, self.range_validator_class)


class ReadOnlyWidgetProxy(object):
    def __init__(self, widget):
        self.widget = widget

    def __getattr__(self, name):
        return getattr(self.widget, name)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('readonly', True)
        # Some html elements also need disabled attribute to achieve the
        # expected UI behaviour.
        kwargs.setdefault('disabled', True)
        return self.widget(field, **kwargs)


class SelectWidget(_Select):
    """
    Add support of choices with ``optgroup`` to the ``Select`` widget.
    """
    @classmethod
    def render_optgroup(cls, value, label, mixed):
        children = []

        for item_value, item_label in label:
            item_html = cls.render_option(item_value, item_label, mixed)
            children.append(item_html)

        html = u'<optgroup label="%s">%s</optgroup>'
        data = (escape(six.text_type(value)), u'\n'.join(children))
        return HTMLString(html % data)

    @classmethod
    def render_option(cls, value, label, mixed):
        """
        Render option as HTML tag, but not forget to wrap options into
        ``optgroup`` tag if ``label`` var is ``list`` or ``tuple``.
        """
        if isinstance(label, (list, tuple)):
            return cls.render_optgroup(value, label, mixed)

        try:
            coerce_func, data = mixed
        except TypeError:
            selected = mixed
        else:
            if isinstance(data, list) or isinstance(data, tuple):
                selected = coerce_func(value) in data
            else:
                selected = coerce_func(value) == data

        options = {'value': value}

        if selected:
            options['selected'] = True

        html = u'<option %s>%s</option>'
        data = (html_params(**options), escape(six.text_type(label)))

        return HTMLString(html % data)
