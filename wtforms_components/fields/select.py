from cgi import escape
from collections import Sequence
from functools import partial
from itertools import repeat
import six
from wtforms.fields import SelectFieldBase
from wtforms.validators import ValidationError
from wtforms.widgets import html_params, HTMLString
from ..widgets import SelectWidget


# def pad(l, pred=identity, padding=0):
#     if not padding:
#         return l
#     return list(l) + list(repeat(pred(l), padding - len(l)))


class EMPTY(object):
    pass



class Choice(object):
    def __init__(self, key, label=EMPTY, value=EMPTY):
        self.key = key
        self.label = self.key if label is EMPTY else label
        self.value = self.key if value is EMPTY else value

    def __repr__(self):
        return '%s(key=%r, label=%r, value=%r)' % (
            self.__class__.__name__,
            self.key,
            self.label,
            self.value
        )


class Choices(object):
    def __init__(self, choices, label=''):
        self.choices = list(map(
            choice_factory,
            choices
        ))
        self.label = label

    def __add__(self, other):
        return Choices([self.choices, other])

    @property
    def values(self):
        for choice in self.choices:
            if isinstance(choice, Choices):
                for value in choice.values:
                    yield value
            else:
                yield choice.value

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


# class ComboChoices(AbstractChoices):
#     def __init__(self, *choices):
#         self.choices = choices

#     @property
#     def values(self):
#         for choices in self.choices:
#             for value in choices.values:
#                 yield value

#     def __getitem__(self, value):
#         for choices in self.choices:
#             try:
#                 return choices[value]
#             except KeyError:
#                 pass
#         raise KeyError(value)

#     def __iter__(self):
#         for choice in chain(*self.choices):
#             yield choice


def choice_factory(data):
    if not isinstance(data, (list, tuple)):
        return Choice(data)
    else:
        data = list(data)
        if isinstance(data[1], (list, tuple)):
            return Choices(data[1], label=data[0])
        else:
            return Choice(*data)


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
       choices
    4. Both fields can render options as disabled
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


# class SelectField(_SelectField):
#     widget = SelectWidget()

#     def iter_choices(self):
#         """
#         We should update how choices are iter to make sure that value from
#         internal list or tuple should be selected.
#         """
#         for value, label in self.concrete_choices:
#             yield (value, label, (self.coerce, self.data))

#     @property
#     def concrete_choices(self):
#         if callable(self.choices):
#             return self.choices()
#         return self.choices

#     @property
#     def choice_values(self):
#         values = []
#         for value, label in self.concrete_choices:
#             if isinstance(label, (list, tuple)):
#                 for subvalue, sublabel in label:
#                     values.append(subvalue)
#             else:
#                 values.append(value)
#         return values

#     def pre_validate(self, form):
#         """
#         Don't forget to validate also values from embedded lists.
#         """
#         values = self.choice_values
#         if (self.data is None and u'' in values) or self.data in values:
#             return True

#         raise ValidationError(self.gettext(u'Not a valid choice'))
