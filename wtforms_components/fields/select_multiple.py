from wtforms.validators import ValidationError

from ..widgets import SelectWidget
from .select import SelectField


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
                    raise ValidationError(
                        self.gettext(
                            "'%(value)s' is not a valid"
                            " choice for this field"
                        ) % dict(value=value)
                    )
