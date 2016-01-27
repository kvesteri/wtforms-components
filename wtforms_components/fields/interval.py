from intervals import (
    DateInterval,
    DateTimeInterval,
    DecimalInterval,
    FloatInterval,
    IntervalException,
    IntInterval
)

from .html5 import StringField


class IntervalField(StringField):
    """
    A string field representing an interval object from
    `intervals`_.

    .. _intervals:
       https://github.com/kvesteri/intervals
    """

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        if self.data:
            return self.data.hyphenized
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == u'' or valuelist[0] == '':
                self.data = None
            else:
                try:
                    self.data = self.interval_class.from_string(valuelist[0])
                except IntervalException:
                    self.data = None
                    raise ValueError(self.gettext(self.error_msg))


class DecimalIntervalField(IntervalField):
    error_msg = u'Not a valid decimal range value'
    interval_class = DecimalInterval


class FloatIntervalField(IntervalField):
    error_msg = u'Not a valid float range value'
    interval_class = FloatInterval


class IntIntervalField(IntervalField):
    error_msg = u'Not a valid int range value'
    interval_class = IntInterval


class DateIntervalField(IntervalField):
    error_msg = u'Not a valid date range value'
    interval_class = DateInterval


class DateTimeIntervalField(IntervalField):
    error_msg = u'Not a valid datetime range value'
    interval_class = DateTimeInterval
