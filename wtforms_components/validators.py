from __future__ import absolute_import

from wtforms import ValidationError
from wtforms.validators import StopValidation

try:
    from validators import email
except ImportError:
    from validators import is_email as email


class ControlStructure(object):
    """
    Base object for validator control structures
    """

    message = None

    def reraise(self, exc):
        if not self.message:
            raise exc
        else:
            raise type(exc)(self.message)


class Chain(ControlStructure):
    """
    Represents a chain of validators, useful when using multiple validators
    with If control structure.

    :param validators:
        list of validator objects
    :param message:
        custom validation error message, if this message is set and some of the
        child validators raise a ValidationError, an exception is being raised
        again with this custom message.
    """
    def __init__(self, validators, message=None):
        self.validators = validators
        if message:
            self.message = message

    def __call__(self, form, field):
        for validator in self.validators:
            try:
                validator(form, field)
            except ValidationError as exc:
                self.reraise(exc)
            except StopValidation as exc:
                self.reraise(exc)


class If(ControlStructure):
    """
    Conditional validator.

    :param condition: callable which takes two arguments form and field
    :param validator: encapsulated validator, this validator is validated
                      only if given condition returns true
    :param message: custom message, which overrides child validator's
                    validation error message
    """
    def __init__(self, condition, validator, message=None):
        self.condition = condition
        self.validator = validator

        if message:
            self.message = message

    def __call__(self, form, field):
        if self.condition(form, field):
            try:
                self.validator(form, field)
            except ValidationError as exc:
                self.reraise(exc)
            except StopValidation as exc:
                self.reraise(exc)


class BaseDateTimeRange(object):
    def __init__(self, min=None, max=None, format='%H:%M', message=None):
        self.min = min
        self.max = max
        self.format = format
        self.message = message

    def __call__(self, form, field):
        data = field.data
        min_ = self.min() if callable(self.min) else self.min
        max_ = self.max() if callable(self.max) else self.max
        if (data is None or (min_ is not None and data < min_) or
                (max_ is not None and data > max_)):
            if self.message is None:
                if max_ is None:
                    self.message = field.gettext(self.greater_than_msg)
                elif min_ is None:
                    self.message = field.gettext(self.less_than_msg)
                else:
                    self.message = field.gettext(self.between_msg)

            raise ValidationError(
                self.message % dict(
                    field_label=field.label,
                    min=min_.strftime(self.format) if min_ else '',
                    max=max_.strftime(self.format) if max_ else ''
                )
            )


class TimeRange(BaseDateTimeRange):
    """
    Same as wtforms.validators.NumberRange but validates date.

    :param min:
        The minimum required value of the time. If not provided, minimum
        value will not be checked.
    :param max:
        The maximum value of the time. If not provided, maximum value
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)s` and `%(max)s` if desired. Useful defaults
        are provided depending on the existence of min and max.
    """

    greater_than_msg = u'Time must be greater than %(min)s.'

    less_than_msg = u'Time must be less than %(max)s.'

    between_msg = u'Time must be between %(min)s and %(max)s.'

    def __init__(self, min=None, max=None, format='%H:%M', message=None):
        super(TimeRange, self).__init__(
            min=min, max=max, format=format, message=message
        )


class DateRange(BaseDateTimeRange):
    """
    Same as wtforms.validators.NumberRange but validates date.

    :param min:
        The minimum required value of the date. If not provided, minimum
        value will not be checked.
    :param max:
        The maximum value of the date. If not provided, maximum value
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)s` and `%(max)s` if desired. Useful defaults
        are provided depending on the existence of min and max.
    """

    greater_than_msg = u'Date must be greater than %(min)s.'

    less_than_msg = u'Date must be less than %(max)s.'

    between_msg = u'Date must be between %(min)s and %(max)s.'

    def __init__(self, min=None, max=None, format='%Y-%m-%d', message=None):
        super(DateRange, self).__init__(
            min=min, max=max, format=format, message=message
        )


class Email(object):
    """
    Validates an email address. This validator is based on `Django's
    email validator`_ and is stricter than the standard email
    validator included in WTForms.

    .. _Django's email validator:
       https://github.com/django/django/blob/master/django/core/validators.py

    :param message:
        Error message to raise in case of a validation error.

    :copyright: (c) Django Software Foundation and individual contributors.
    :license: BSD
    """
    domain_whitelist = ['localhost']

    def __init__(self, message=None, whitelist=None):
        self.message = message
        if whitelist is not None:
            self.domain_whitelist = whitelist

    def __call__(self, form, field):
        if not email(field.data, self.domain_whitelist):
            if self.message is None:
                self.message = field.gettext(u'Invalid email address.')
            raise ValidationError(self.message)
