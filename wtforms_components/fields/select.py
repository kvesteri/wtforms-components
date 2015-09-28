from wtforms import SelectField as _SelectField
from wtforms.validators import ValidationError

from ..widgets import SelectWidget


class SelectField(_SelectField):
    """
    Add support of ``optgroup``'s' to default WTForms' ``SelectField`` class.

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
        if (self.data is None and u'' in values) or self.data in values:
            return True

        raise ValidationError(self.gettext(u'Not a valid choice'))
