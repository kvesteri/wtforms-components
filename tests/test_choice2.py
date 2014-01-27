try:
    from collections import ChainMap
except ImportError:
    import UserDict

    class ChainMap(UserDict.DictMixin):
        """Combine multiple mappings for sequential lookup.

        For example, to emulate Python's normal lookup sequence:

            import __builtin__
            pylookup = ChainMap(locals(), globals(), vars(__builtin__))
        """
        def __init__(self, *maps):
            self.maps = maps
        def __getitem__(self, key):
            for mapping in self.maps:
                try:
                    return mapping[key]
                except KeyError:
                    pass
            raise KeyError(key)
        def keys(self):
            return list(self.iterkeys())
        def iterkeys(self):
            return (k for m in self.maps for k in m.iterkeys())
        def values(self):
            return list(self.itervalues())
        def itervalues(self):
            return (v for m in self.maps for v in m.itervalues())

from collections import Mapping
from ordereddict import OrderedDict
from wtforms.compat import text_type
from wtforms import SelectField as _SelectField


class Choice(object):
    def __init__(self, label, value):
        self.value = value
        self.label = label

    def __eq__(self, other):
        if isinstance(other, Choice):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not (self == other)


def leaf(obj, key):
    item = obj.get(key, None)

    if item is None or isinstance(item, Mapping):
        for subkey in obj.__iter__():
            item = obj.get(subkey, None)
            if isinstance(item, Mapping):
                try:
                    return leaf(item, key)
                except KeyError:
                    pass
    else:
        return item
    raise KeyError(key)


class Choices(OrderedDict):
    def leaf(self, key):
        return leaf(self, key)

    def __setitem__(self, key, value):
        if not isinstance(value, Choice):
            value = Choice(label=value, value=key)
        super(Choices, self).__setitem__(key, value)


class SelectField(_SelectField):
    def __init__(self, label=None, validators=None, coerce=text_type, choices=None, **kwargs):
        super(SelectField, self).__init__(label, validators, **kwargs)
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
            self._choices = deep_dict(choices, Choices)

    def iter_choices(self):
        for value, label in self.choices:
            yield (value, label, self.coerce(value) == self.data)

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
                raise ValueError(self.gettext('Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == v:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


def deep_dict(seq, f=dict):
    def pair_f(pair):
        k, v = pair
        if isinstance(v, (list, tuple)):
            return k, deep_dict(v, f)
        return k, v
    return f(map(pair_f, seq))


class TestChoices(object):
    def test_choices_length(self):
        assert len(Choices([(1, 1)])) == 1

    def test_deep_sequence_conversion(self):
        seq = [
            (1,
                (
                    (2, 1),
                    (3, 1),
                    (4, 1)
                )
            ),
            (5, 1)
            (6,
                (
                    (8, 1),
                    (8, 1),
                )
            ),
            (7,
                (
                    (9,
                        (
                            (10, 1),
                            (11, 1)
                        ),
                    ),
                )
            )
        ]
        choices = deep_dict(seq, Choices)
        assert 2 in choices

# class Choices2(object):
#     def __init__(self, choices, label=''):
#         self.choices = list(map(
#             choice_factory,
#             choices
#         ))
#         self.label = label

#     def __add__(self, other):
#         if isinstance(other, Choice):
#             return Choices(self.choices + [other])
#         elif isinstance(other, Choices):
#             return ChoicesChain(self, other)
#         return NotImplemented

#     def __radd__(self, other):
#         if isinstance(other, Choice):
#             return Choices([other] + self.choices)
#         return NotImplemented

#     @property
#     def values(self):
#         for choice in self.choices:
#             if isinstance(choice, Choices):
#                 for value in choice.values:
#                     yield value
#             else:
#                 yield choice.value

#     def __len__(self):
#         return len(self.choices)

#     def __getitem__(self, key):
#         for choice in self.choices:
#             if isinstance(choice, Choice):
#                 if choice.key == six.text_type(key):
#                     return choice.value
#             else:
#                 try:
#                     return choice[key]
#                 except KeyError:
#                     pass
#         raise KeyError(key)

#     def __iter__(self):
#         for choice in self.choices:
#             yield choice

#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, list(self.choices))
