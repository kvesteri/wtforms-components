import datetime

from wtforms import Form
from wtforms.fields import FormField

from .html5 import DateField
from .time import TimeField

try:
    from wtforms.utils import unset_value as _unset_value
except ImportError:
    from wtforms.fields import _unset_value


class Date():
    date = None
    time = None


class SplitDateTimeField(FormField):
    def __init__(self, label=None, validators=None, separator='-', **kwargs):
        FormField.__init__(
            self,
            datetime_form(kwargs.pop('datetime_form', {})),
            label=label,
            validators=validators,
            separator=separator,
            **kwargs
        )

    def process(self, formdata, data=_unset_value, extra_filters=None):
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

        kwargs = dict()
        if extra_filters is not None:
            # do not enforce extra_filters=None injection to wtforms<3
            kwargs['extra_filters'] = extra_filters
        FormField.process(self, formdata, data=obj, **kwargs)

    def populate_obj(self, obj, name):
        if hasattr(obj, name):
            date = self.date.data
            hours, minutes = self.time.data.hour, self.time.data.minute
            setattr(obj, name, datetime.datetime(
                date.year, date.month, date.day, hours, minutes
            ))


def datetime_form(options):
    options.setdefault('date', {})
    options.setdefault('time', {})
    options['date'].setdefault('label', u'Date')
    options['time'].setdefault('label', u'Time')
    base_form = options.get('base_form', Form)

    class DateTimeForm(base_form):
        date = DateField(**options['date'])
        time = TimeField(**options['time'])
    return DateTimeForm
