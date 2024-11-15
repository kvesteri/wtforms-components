from validators import email
from wtforms import ValidationError
from wtforms.validators import StopValidation


class ControlStructure:
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


class BaseDateTimeRange:
    def __init__(self, min=None, max=None, format="%H:%M", message=None):
        self.min = min
        self.max = max
        self.format = format
        self.message = message

    def __call__(self, form, field):
        data = field.data
        min_ = self.min() if callable(self.min) else self.min
        max_ = self.max() if callable(self.max) else self.max
        if (
            data is None
            or (min_ is not None and data < min_)
            or (max_ is not None and data > max_)
        ):
            if self.message is None:
                if max_ is None:
                    self.message = field.gettext(self.greater_than_msg)
                elif min_ is None:
                    self.message = field.gettext(self.less_than_msg)
                else:
                    self.message = field.gettext(self.between_msg)

            raise ValidationError(
                self.message
                % dict(
                    field_label=field.label,
                    min=min_.strftime(self.format) if min_ else "",
                    max=max_.strftime(self.format) if max_ else "",
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

    greater_than_msg = "Time must be greater than %(min)s."

    less_than_msg = "Time must be less than %(max)s."

    between_msg = "Time must be between %(min)s and %(max)s."

    def __init__(self, min=None, max=None, format="%H:%M", message=None):
        super().__init__(min=min, max=max, format=format, message=message)


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

    greater_than_msg = "Date must be equal to or later than %(min)s."

    less_than_msg = "Date must be equal to or earlier than %(max)s."

    between_msg = "Date must be between %(min)s and %(max)s."

    def __init__(self, min=None, max=None, format="%Y-%m-%d", message=None):
        super().__init__(min=min, max=max, format=format, message=message)


class Email:
    """
    Validates an email address.
    This validator is is stricter than the standard email
    validator included in WTForms.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not email(field.data):
            message = self.message
            if message is None:
                message = field.gettext("Invalid email address.")
            raise ValidationError(message)
