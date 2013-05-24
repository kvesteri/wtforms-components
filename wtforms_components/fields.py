import datetime
import time
import phonenumbers
from colour import Color
from wtforms import Form
from wtforms.fields import (
    Field,
    FormField,
    HiddenField,
    SelectField as _SelectField,
    StringField
)
from wtforms.fields import html5
from wtforms.fields.core import _unset_value
from wtforms.validators import ValidationError
from sqlalchemy_utils import PhoneNumber, NumberRange, NumberRangeException
from .widgets import (
    ColorInput,
    DateInput,
    DateTimeInput,
    DateTimeLocalInput,
    EmailInput,
    NumberInput,
    SelectWidget,
    TelInput,
    TimeInput,
    RangeInput,
    SearchInput,
)


class EmailField(StringField):
    widget = EmailInput()


class IntegerField(html5.IntegerField):
    widget = NumberInput()


class DecimalField(html5.DecimalField):
    widget = NumberInput()


class DateTimeLocalField(html5.DateTimeField):
    widget = DateTimeLocalInput()


class DateTimeField(html5.DateTimeField):
    widget = DateTimeInput()


class DateField(html5.DateField):
    widget = DateInput()


class IntegerSliderField(html5.IntegerRangeField):
    widget = RangeInput()


class DecimalSliderField(html5.DecimalRangeField):
    widget = RangeInput()


class SearchField(html5.SearchField):
    widget = SearchInput()


class SelectField(_SelectField):
    """
    Add support of ``optgorup``'s' to default WTForms' ``SelectField`` class.

    So, next choices would be supported as well::

        (
            ('Fruits', (
                ('apple', 'Apple'),
                ('peach', 'Peach'),
                ('pear', 'Pear')
            )),
            ('Vegetables', (
                ('cucumber', 'Cucumber'),
                ('potato', 'Potato'),
                ('tomato', 'Tomato'),
            ))
        )

    Also supports lazy choices (callables that return an iterable)
    """
    widget = SelectWidget()

    def iter_choices(self):
        """
        We should update how choices are iter to make sure that value from
        internal list or tuple should be selected.
        """
        for value, label in self.concrete_choices:
            yield (value, label, (self.coerce, self.data))

    @property
    def concrete_choices(self):
        if callable(self.choices):
            return self.choices()
        return self.choices

    @property
    def choice_values(self):
        values = []
        for value, label in self.concrete_choices:
            if isinstance(label, (list, tuple)):
                for subvalue, sublabel in label:
                    values.append(subvalue)
            else:
                values.append(value)
        return values

    def pre_validate(self, form):
        """
        Don't forget to validate also values from embedded lists.
        """
        values = self.choice_values
        if self.data is None and u'' in values:
            return True

        if self.data in values:
            return True

        raise ValidationError(self.gettext(u'Not a valid choice'))


class SelectMultipleField(SelectField):
    """
    No different from a normal select field, except this one can take (and
    validate) multiple choices.  You'll need to specify the HTML `rows`
    attribute to the select field when rendering.
    """
    widget = SelectWidget(multiple=True)

    def process_data(self, value):
        try:
            self.data = list(self.coerce(v) for v in value)
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        try:
            self.data = list(self.coerce(x) for x in valuelist)
        except ValueError:
            raise ValueError(
                self.gettext(
                    'Invalid choice(s): one or more data inputs '
                    'could not be coerced'
                )
            )

    def pre_validate(self, form):
        if self.data:
            values = self.choice_values
            for value in self.data:
                if value not in values:
                    raise ValueError(
                        self.gettext(
                            "'%(value)s' is not a valid"
                            " choice for this field"
                        ) % dict(value=value)
                    )


class TimeField(Field):
    """
    A text field which stores a `datetime.time` matching a format.
    """
    widget = TimeInput()
    error_msg = 'Not a valid time.'

    def __init__(self, label=None, validators=None, format='%H:%M', **kwargs):
        super(TimeField, self).__init__(label, validators, **kwargs)
        self.format = format

    def _value(self):
        if self.raw_data:
            return ' '.join(self.raw_data)
        else:
            return self.data and self.data.strftime(self.format) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            time_str = ' '.join(valuelist)
            try:
                self.data = datetime.time(
                    *time.strptime(time_str, self.format)[3:5]
                )
            except ValueError:
                self.data = None
                raise ValueError(self.gettext(self.error_msg))


class Date():
    date = None
    time = None


class SplitDateTimeField(FormField):
    def __init__(self, label=None, validators=None, separator='-', **kwargs):
        FormField.__init__(
            self,
            datetime_form(kwargs.get('datetime_form', {})),
            label=label,
            validators=validators,
            separator=separator,
            **kwargs
        )

    def process(self, formdata, data=_unset_value):
        if data is _unset_value:
            try:
                data = self.default()
            except TypeError:
                data = self.default
        if data:
            obj = Date()
            obj.date = data.date()
            obj.time = data.time()
        else:
            obj = None
        FormField.process(self, formdata, data=obj)

    def populate_obj(self, obj, name):
        if hasattr(obj, name):
            date = self.date.data
            hours, minutes = self.time.data.tm_hour, self.time.data.tm_min
            setattr(obj, name, datetime(
                date.year, date.month, date.day, hours, minutes
            ))


def datetime_form(options):
    options.setdefault('date', {})
    options.setdefault('time', {})
    options['date'].setdefault('label', u'Date')
    options['time'].setdefault('label', u'Time')

    class DateTimeForm(Form):
        date = DateField(options['date'].label, **options['date'])
        time = TimeField(options['time'].label, **options['time'])
    return DateTimeForm


class PhoneNumberField(StringField):
    """
    A string field representing a PhoneNumber object from
    `SQLAlchemy-Utils`_.

    .. _SQLAlchemy-Utils:
       https://github.com/kvesteri/sqlalchemy-utils

    :param country_code:
        Country code of the phone number.
    :param display_format:
        The format in which the phone number is displayed.
    """
    widget = TelInput()
    error_msg = u'Not a valid phone number value'

    def __init__(self, label=None, validators=None, country_code='US',
                 display_format='national',
                 **kwargs):
        super(PhoneNumberField, self).__init__(label, validators, **kwargs)
        self.country_code = country_code
        self.display_format = display_format

    def _value(self):
        # self.data holds a PhoneNumber object, use it before falling back
        # to self.rawdata which holds a string
        if self.data:
            return getattr(self.data, self.display_format)
        elif self.raw_data:
            return self.raw_data[0]
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == u'':
                self.data = None
            else:
                try:
                    self.data = PhoneNumber(
                        valuelist[0],
                        self.country_code
                    )
                    if not self.data.is_valid_number():
                        self.data = None
                        raise ValueError(self.gettext(self.error_msg))
                except phonenumbers.phonenumberutil.NumberParseException:
                    self.data = None
                    raise ValueError(self.gettext(self.error_msg))


class NumberRangeField(StringField):
    """
    A string field representing a NumberRange object from
    `SQLAlchemy-Utils`_.

    .. _SQLAlchemy-Utils:
       https://github.com/kvesteri/sqlalchemy-utils
    """
    error_msg = u'Not a valid number range value'

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data:
            return str(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == u'' or valuelist[0] == '':
                self.data = None
            else:
                try:
                    self.data = NumberRange.from_str(valuelist[0])
                except NumberRangeException:
                    self.data = None
                    raise ValueError(self.gettext(self.error_msg))


class ColorField(StringField):
    """
    A string field representing a Color object from python colour package.

    .. _colours:
       https://github.com/vaab/colour

    Represents an ``<input type="color">``.
    """
    widget = ColorInput()

    error_msg = u'Not a valid color.'

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data:
            return str(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == u'' or valuelist[0] == '':
                self.data = None
            else:
                try:
                    self.data = Color(valuelist[0])
                except AttributeError:
                    self.data = None
                    raise ValueError(self.gettext(self.error_msg))


class PassiveHiddenField(HiddenField):
    """
    HiddenField that does not populate obj values.
    """
    def populate_obj(self, obj, name):
        pass
