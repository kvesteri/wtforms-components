from cgi import escape
from collections import Sequence
from functools import partial
from itertools import chain, repeat
import six
from wtforms.fields import SelectFieldBase
from wtforms.validators import ValidationError
from wtforms.widgets import html_params, HTMLString
try:
    from wtforms.utils import unset_value as _unset_value
except ImportError:
    from wtforms.fields import _unset_value
from ..widgets import SelectWidget


class Choice(object):
    def __init__(self, key, label=_unset_value, value=_unset_value):
        self.key = key
        self.label = self.key if label is _unset_value else label
        self.value = self.key if value is _unset_value else value

    def __repr__(self):
        return '%s(key=%r, label=%r, value=%r)' % (
            self.__class__.__name__,
            self.key,
            self.label,
            self.value
        )

    def __add__(self, other):
        if not isinstance(other, Choice):
            return NotImplemented
        return Choices([self, other])


class Chain(object):
    def __init__(self, *iterables):
        self.iterables = iterables

    def __iter__(self):
        for iterable in self.iterables:
            for value in iterable:
                yield value

    def __contains__(self, value):
        return any(value in iterable for iterable in self.iterables)

    def __len__(self):
        return sum(map(len, self.iterables))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, list(self.iterables))


class ChoicesChain(Chain):
    @property
    def values(self):
        for choices in self.iterables:
            for value in choice.values:
                yield value

    def __add__(self, other):
        iterables = list(self.iterables)
        if isinstance(other, Choice):
            iterables.append(Choices([other]))
            return ChoicesChain(*iterables)
        elif isinstance(other, Choices):
            iterables.append(other)
            return ChoicesChain(*iterables)
        elif isinstance(other, ChoicesChain):
            iterables.extend(other.iterables)
            return ChoicesChain(*iterables)
        return NotImplemented

    def __radd__(self, other):
        iterables = list(self.iterables)
        if isinstance(other, Choice):
            iterables.insert(0, Choices([other]))
            return ChoicesChain(*iterables)
        elif isinstance(other, Choices):
            iterables.insert(0, other)
            return ChoicesChain(*iterables)
        return NotImplemented


class Choices(object):
    def __init__(self, choices, label=''):
        self.choices = list(map(
            choice_factory,
            choices
        ))
        self.label = label

    def __add__(self, other):
        if isinstance(other, Choice):
            return Choices(self.choices + [other])
        elif isinstance(other, Choices):
            return ChoicesChain(self, other)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, Choice):
            return Choices([other] + self.choices)
        return NotImplemented

    @property
    def values(self):
        for choice in self.choices:
            if isinstance(choice, Choices):
                for value in choice.values:
                    yield value
            else:
                yield choice.value

    def __len__(self):
        return len(self.choices)

    def __getitem__(self, key):
        for choice in self.choices:
            if isinstance(choice, Choice):
                if choice.key == six.text_type(key):
                    return choice.value
            else:
                try:
                    return choice[key]
                except KeyError:
                    pass
        raise KeyError(key)

    def __iter__(self):
        for choice in self.choices:
            yield choice

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, list(self.choices))


def choice_factory(data):
    if isinstance(data, (list, tuple)):
        data = list(data)
        if isinstance(data[1], (list, tuple)):
            return Choices(data[1], label=data[0])
        else:
            return Choice(*data)
    else:
        if isinstance(data, Choice):
            return data
        else:
            return Choice(data)


class SelectField(SelectFieldBase):
    """
    Compared to old wtforms.fields.SelectField this class offers the following
    features and improvments:

    1. SelectField and SelectMultiple field can render optgroups

    ::

        choices = (
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

        SelectField(choices=choices)

    2. Both fields accepts callables as choices allowing lazy evaluation of
       choices
    3. The Choices class. Both fields can combine query choices to regular
       choices.
    """
    widget = SelectWidget()

    def __init__(
        self,
        label=None,
        validators=None,
        coerce=six.text_type,
        choices=None,
        **kwargs
    ):
        SelectFieldBase.__init__(self, label, validators, **kwargs)
        self.coerce = coerce
        self.choices = choices

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, data):
        choices = data() if callable(data) else data
        if isinstance(choices, Choices):
            self._choices = choices
        else:
            self._choices = Choices(choices)

    def process_data(self, value):
        try:
            self.data = self.coerce(value)
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = self.coerce(valuelist[0])
            except ValueError:
                raise ValueError(
                    self.gettext('Invalid Choice: could not coerce')
                )

    def iter_choices(self):
        for choice in self.choices:
            yield choice

    def __iter__(self):
        opts = dict(
            widget=self.option_widget,
            _name=self.name,
            _form=None,
            _meta=self.meta
        )
        for i, choice in enumerate(self.iter_choices()):
            opt = self._Option(
                label=choice.label,
                id='%s-%d' % (self.id, i),
                **opts
            )
            opt.process(None, value)
            opt.checked = self.data == choice.value
            yield opt

    def pre_validate(self, form):
        if not self.data in self.choices.values:
             raise ValueError(self.gettext('Not a valid choice'))
