from cgi import escape
from wtforms.widgets import (
    HTMLString,
    html_params,
    Select as _Select
)
from wtforms.validators import NumberRange, DataRequired
from wtforms.widgets import Input
from .validators import DateRange, TimeRange


def min_max(field, validator_class):
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
    for validator in field.validators:
        if isinstance(validator, validator_class):
            return True
    return False


class HTML5Input(Input):
    def __call__(self, field, **kwargs):
        if has_validator(field, DataRequired):
            kwargs.setdefault('required', True)
        return super(HTML5Input, self).__call__(field, **kwargs)


class BaseDateTimeInput(HTML5Input):
    """
    Base class for TimeInput, DateTimeLocalInput, DateTimeInput and
    DateInput widgets
    """
    range_validator_class = DateRange

    def __call__(self, field, **kwargs):
        for key, value in min_max(field, self.range_validator_class).items():
            kwargs.setdefault(key, value.strftime(self.format))

        return super(BaseDateTimeInput, self).__call__(field, **kwargs)


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

    def __call__(self, field, **kwargs):
        for key, value in min_max(field, NumberRange).items():
            kwargs.setdefault(key, value)

        return super(NumberInput, self).__call__(field, **kwargs)


class ReadOnlyWidgetProxy(object):
    def __init__(self, widget):
        self.widget = widget

    def __getattr__(self, name):
        return getattr(self.widget, name)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('readonly', True)
        return self.widget(field, **kwargs)


class SelectWidget(_Select):
    """
    Add support of choices with ``optgroup`` to the ``Select`` widget.
    """
    @classmethod
    def render_option(cls, value, label, mixed):
        """
        Render option as HTML tag, but not forget to wrap options into
        ``optgroup`` tag if ``label`` var is ``list`` or ``tuple``.
        """
        if isinstance(label, (list, tuple)):
            children = []

            for item_value, item_label in label:
                item_html = cls.render_option(item_value, item_label, mixed)
                children.append(item_html)

            html = u'<optgroup label="%s">%s</optgroup>'
            data = (escape(unicode(value)), u'\n'.join(children))
        else:
            coerce_func, data = mixed
            if isinstance(data, list) or isinstance(data, tuple):
                selected = coerce_func(value) in data
            else:
                selected = coerce_func(value) == data

            options = {'value': value}

            if selected:
                options['selected'] = u'selected'

            html = u'<option %s>%s</option>'
            data = (html_params(**options), escape(unicode(label)))

        return HTMLString(html % data)
