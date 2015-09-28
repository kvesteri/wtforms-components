from __future__ import absolute_import

from collections import Iterable, Mapping

import six
from sqlalchemy import Column
from sqlalchemy.orm.attributes import InstrumentedAttribute
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


class Unique(object):
    """Checks field values unicity against specified table fields.

    :param column:
        InstrumentedAttribute object, eg. User.name, or
        Column object, eg. user.c.name, or
        a field name, eg. 'name' or
        a tuple of InstrumentedAttributes, eg. (User.name, User.email) or
        a dictionary mapping field names to InstrumentedAttributes, eg.
        {
            'name': User.name,
            'email': User.email
        }
    :param get_session:
        A function that returns a SQAlchemy Session. This parameter is not
        needed if the given model supports Flask-SQLAlchemy styled query
        parameter.
    :param message:
        The error message.
    """
    field_flags = ('unique', )

    def __init__(self, column, get_session=None, message=None):
        self.column = column
        self.message = message
        self.get_session = get_session

    @property
    def query(self):
        self._check_for_session(self.model)
        if self.get_session:
            return self.get_session().query(self.model)
        elif hasattr(self.model, 'query'):
            return getattr(self.model, 'query')
        else:
            raise Exception(
                'Validator requires either get_session or Flask-SQLAlchemy'
                ' styled query parameter'
            )

    def _check_for_session(self, model):
        if not hasattr(model, 'query') and not self.get_session:
            raise Exception('Could not obtain SQLAlchemy session.')

    def _syntaxes_as_tuples(self, form, field, column):
        """Converts a set of different syntaxes into a tuple of tuples"""
        if isinstance(column, six.string_types):
            return ((column, getattr(form.Meta.model, column)),)
        elif isinstance(column, Mapping):
            return tuple(
                (x[0], self._syntaxes_as_tuples(form, field, x[1])[0][1])
                for x in column.items()
            )
        elif isinstance(column, Iterable):
            return tuple(
                self._syntaxes_as_tuples(form, field, x)[0]
                for x in column
            )
        elif isinstance(column, (Column, InstrumentedAttribute)):
            return ((column.key, column),)
        else:
            raise TypeError("Invalid syntax for column")

    def __call__(self, form, field):
        columns = self._syntaxes_as_tuples(form, field, self.column)
        self.model = columns[0][1].class_
        query = self.query
        for field_name, column in columns:
            query = query.filter(column == form[field_name].data)
        obj = query.first()

        if not hasattr(form, '_obj') or (obj and not form._obj == obj):
            if self.message is None:
                self.message = field.gettext(u'Already exists.')
            raise ValidationError(self.message)


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
