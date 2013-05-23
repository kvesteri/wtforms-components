from cgi import escape
from wtforms.widgets import (
    HTMLString,
    html_params,
    Select as _Select
)
from wtforms.validators import NumberRange, DataRequired
from wtforms.widgets import html5
from .validators import DateRange


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


class DateTimeLocalInput(html5.DateTimeLocalInput):
    """
    Renders an input with type "datetime-local".

    Adds min and max html5 field parameters based on field's DateRange
    validator.
    """
    def __call__(self, field, **kwargs):
        if has_validator(field, DataRequired):
            kwargs.setdefault('required', True)
        for key, value in min_max(field, DateRange).items():
            kwargs.setdefault(key, value.strftime(field.format))

        return super(DateTimeLocalInput, self).__call__(field, **kwargs)


class DateTimeInput(html5.DateTimeInput):
    """
    Renders an input with type "datetime".

    Adds min and max html5 field parameters based on field's DateRange
    validator.
    """
    def __call__(self, field, **kwargs):
        if has_validator(field, DataRequired):
            kwargs.setdefault('required', True)
        for key, value in min_max(field, DateRange).items():
            kwargs.setdefault(key, value.strftime(field.format))

        return super(DateTimeInput, self).__call__(field, **kwargs)


class DateInput(html5.DateInput):
    """
    Renders an input with type "date".

    Adds min and max html5 field parameters based on field's DateRange
    validator.
    """
    def __call__(self, field, **kwargs):
        if has_validator(field, DataRequired):
            kwargs.setdefault('required', True)
        for key, value in min_max(field, DateRange).items():
            kwargs.setdefault(key, value.strftime(field.format))

        return super(DateInput, self).__call__(field, **kwargs)


class NumberInput(html5.NumberInput):
    """
    Renders an input with type "number".

    Adds min and max html5 field parameters based on field's NumberRange
    validator.
    """
    def __call__(self, field, **kwargs):
        if has_validator(field, DataRequired):
            kwargs.setdefault('required', True)
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
