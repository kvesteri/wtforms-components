def is_scalar(value):
    return isinstance(value, (type(None), str, int, float, bool))


def null_or_unicode(value):
    return str(value) or None


def null_or_int(value):
    try:
        return int(value)
    except TypeError:
        return None


class Chain:
    """
    Generic chain class. Very similar to itertools.chain except this object
    can be iterated over multiple times.
    """

    def __init__(self, *iterables):
        self.iterables = iterables

    def __iter__(self):
        for iterable in self.iterables:
            yield from iterable

    def __contains__(self, value):
        return any(value in iterable for iterable in self.iterables)

    def __len__(self):
        return sum(map(len, self.iterables))

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self.iterables)!r})"
