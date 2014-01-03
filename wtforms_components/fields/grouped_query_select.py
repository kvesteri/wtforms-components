from itertools import groupby
import six
from wtforms.validators import ValidationError

from .select import SelectField
from ..widgets import SelectWidget


class GroupedQuerySelectField(SelectField):
    widget = SelectWidget()

    def __init__(self, label=None, validators=None, query_factory=None,
                 get_pk=None, get_label=None, get_group=None,
                 allow_blank=False, blank_text='', **kwargs):
        super(GroupedQuerySelectField, self).__init__(
            label,
            validators,
            coerce=lambda x: x,
            **kwargs
        )

        raise Exception(
            'GroupedQuerySelectField has been deprecated. Use new Choices '
            'objects with regular SelectFields.'
        )
