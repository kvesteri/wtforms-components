from copy import copy

from markupsafe import Markup, escape
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import Input, html_params
from wtforms.widgets import Select as _Select

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
        data["min"] = max(min_values)
    if max_values:
        data["max"] = min(max_values)
    return data


def has_validator(field, validator_class):
    """
    Returns whether or not given field has an instance of given validator class
    in the validators property.

    :param field: WTForms Field object
    :param validator_class: WTForms Validator class
    """
    return any(
        [isinstance(validator, validator_class) for validator in field.validators]
    )


class HTML5Input(Input):
    validation_attrs = ["required", "disabled"]

    def __init__(self, **kwargs):
        self.options = kwargs

    def __call__(self, field, **kwargs):
        if has_validator(field, DataRequired):
            kwargs.setdefault("required", True)

        for key, value in self.range_validators(field).items():
            kwargs.setdefault(key, value)

        if hasattr(field, "widget_options"):
            for key, value in self.field.widget_options:
                kwargs.setdefault(key, value)

        options_copy = copy(self.options)
        options_copy.update(kwargs)
        return super().__call__(field, **options_copy)

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
        if "min" in data:
            data["min"] = data["min"].strftime(self.format)
        if "max" in data:
            data["max"] = data["max"].strftime(self.format)
        return data


class TextInput(HTML5Input):
    input_type = "text"


class SearchInput(HTML5Input):
    """
    Renders an input with type "search".
    """

    input_type = "search"


class MonthInput(HTML5Input):
    """
    Renders an input with type "month".
    """

    input_type = "month"


class WeekInput(HTML5Input):
    """
    Renders an input with type "week".
    """

    input_type = "week"


class RangeInput(HTML5Input):
    """
    Renders an input with type "range".
    """

    input_type = "range"


class URLInput(HTML5Input):
    """
    Renders an input with type "url".
    """

    input_type = "url"


class ColorInput(HTML5Input):
    """
    Renders an input with type "color".
    """

    input_type = "color"


class TelInput(HTML5Input):
    """
    Renders an input with type "tel".
    """

    input_type = "tel"


class EmailInput(HTML5Input):
    """
    Renders an input with type "email".
    """

    input_type = "email"


class TimeInput(BaseDateTimeInput):
    """
    Renders an input with type "time".

    Adds min and max html5 field parameters based on field's TimeRange
    validator.
    """

    input_type = "time"
    range_validator_class = TimeRange
    format = "%H:%M:%S"


class DateTimeLocalInput(BaseDateTimeInput):
    """
    Renders an input with type "datetime-local".

    Adds min and max html5 field parameters based on field's DateRange
    validator.
    """

    input_type = "datetime-local"
    format = "%Y-%m-%dT%H:%M:%S"


class DateTimeInput(BaseDateTimeInput):
    """
    Renders an input with type "datetime".

    Adds min and max html5 field parameters based on field's DateRange
    validator.
    """

    input_type = "datetime"
    format = "%Y-%m-%dT%H:%M:%SZ"


class DateInput(BaseDateTimeInput):
    """
    Renders an input with type "date".

    Adds min and max html5 field parameters based on field's DateRange
    validator.
    """

    input_type = "date"
    format = "%Y-%m-%d"


class NumberInput(HTML5Input):
    """
    Renders an input with type "number".

    Adds min and max html5 field parameters based on field's NumberRange
    validator.
    """

    input_type = "number"
    range_validator_class = NumberRange

    def range_validators(self, field):
        return min_max(field, self.range_validator_class)


class ReadOnlyWidgetProxy:
    def __init__(self, widget):
        self.widget = widget

    def __getattr__(self, name):
        return getattr(self.widget, name)

    def __call__(self, field, **kwargs):
        kwargs.setdefault("readonly", True)
        # Some html elements also need disabled attribute to achieve the
        # expected UI behaviour.
        kwargs.setdefault("disabled", True)
        return self.widget(field, **kwargs)


class SelectWidget(_Select):
    """
    ``Select`` widget that renders ``optgroup``'s mixed with ungrouped options.

    Uses the field's ``has_groups()`` and ``iter_groups()`` methods, where a
    group label of ``None`` means the options are not wrapped in an
    ``optgroup``.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if self.multiple:
            kwargs["multiple"] = True
        flags = getattr(field, "flags", {})
        for k in dir(flags):
            if k in self.validation_attrs and k not in kwargs:
                kwargs[k] = getattr(flags, k)

        if field.has_groups():
            groups = field.iter_groups()
        else:
            groups = [(None, field.iter_choices())]

        html = [f"<select {html_params(name=field.name, **kwargs)}>"]
        for group, choices in groups:
            if group is not None:
                html.append(f"<optgroup {html_params(label=group)}>")
            # WTForms 3.3 yields ``Choice`` named tuples, older versions tuples.
            for value, label, selected, render_kw in choices:
                html.append(
                    self.render_option(value, label, selected, **(render_kw or {}))
                )
            if group is not None:
                html.append("</optgroup>")
        html.append("</select>")
        return Markup("".join(html))

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        options = {"value": value, **kwargs}
        if selected:
            options["selected"] = True
        return Markup(f"<option {html_params(**options)}>{escape(label)}</option>")
