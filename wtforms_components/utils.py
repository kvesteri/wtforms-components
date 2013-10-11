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
