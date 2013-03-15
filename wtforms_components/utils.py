def is_scalar(value):
    return isinstance(value, (type(None), str, int, float, bool, unicode))


def null_or_unicode(value):
    return unicode(value) or None


def null_or_int(value):
    try:
        return int(value)
    except TypeError:
        return None
