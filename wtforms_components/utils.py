import six


def is_scalar(value):
    return isinstance(value, (type(None), six.string_types, int, float, bool))


def null_or_unicode(value):
    return six.text_type(value) or None


def null_or_int(value):
    try:
        return int(value)
    except TypeError:
        return None


class Chain(object):
    """
    Generic chain class. Very similar to itertools.chain except this object
    can be iterated over multiple times.
    """
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
