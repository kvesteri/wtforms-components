from wtforms import SelectField as _SelectField
from wtforms.validators import ValidationError

try:
    from wtforms.fields.choices import Choice
except ImportError:  # WTForms < 3.3
    from collections import namedtuple

    Choice = namedtuple("Choice", "value label selected render_kw")

from ..widgets import SelectWidget


class SelectField(_SelectField):
    """
    Add support of ``optgroup``'s' to default WTForms' ``SelectField`` class.

    So, next choices would be supported as well::

        (
            (
                "Fruits",
                (
                    ("apple", "Apple"),
                    ("peach", "Peach"),
                    ("pear", "Pear"),
                ),
            ),
            (
                "Vegetables",
                (
                    ("cucumber", "Cucumber"),
                    ("potato", "Potato"),
                    ("tomato", "Tomato"),
                ),
            ),
        )

    Also supports lazy choices (callables that return an iterable)
    """

    widget = SelectWidget()

    def __init__(self, *args, choices=None, **kwargs):
        # Set choices after init, so that WTForms doesn't parse or warn about
        # the nested choices it doesn't understand.
        super().__init__(*args, **kwargs)
        if choices is not None and not callable(choices):
            # Materialize iterators, as choices are iterated more than once.
            choices = list(choices)
        self.choices = choices

    def _choice(self, value, label):
        if isinstance(self.data, list | tuple):
            selected = self.coerce(value) in self.data
        else:
            selected = self.coerce(value) == self.data
        return Choice(value, label, selected, {})

    def _flat_choices(self):
        for value, label in self.concrete_choices:
            if isinstance(label, list | tuple):
                yield from label
            else:
                yield value, label

    def iter_choices(self):
        for value, label in self._flat_choices():
            yield self._choice(value, label)

    def has_groups(self):
        return any(
            isinstance(label, list | tuple) for _, label in self.concrete_choices
        )

    def iter_groups(self):
        """
        Yield ``(group_label, choices)`` pairs. Consecutive ungrouped choices
        are yielded with a ``None`` group label.
        """
        ungrouped = []
        for value, label in self.concrete_choices:
            if isinstance(label, list | tuple):
                if ungrouped:
                    yield None, ungrouped
                    ungrouped = []
                yield value, [self._choice(v, lbl) for v, lbl in label]
            else:
                ungrouped.append(self._choice(value, label))
        if ungrouped:
            yield None, ungrouped

    @property
    def concrete_choices(self):
        if callable(self.choices):
            return self.choices()
        return self.choices

    @property
    def choice_values(self):
        return [value for value, _ in self._flat_choices()]

    def pre_validate(self, form):
        """
        Don't forget to validate also values from embedded lists.
        """
        values = self.choice_values
        if (self.data is None and "" in values) or self.data in values:
            return True

        raise ValidationError(self.gettext("Not a valid choice"))
