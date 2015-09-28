from itertools import groupby

import six
from sqlalchemy.orm.util import identity_key
from wtforms.validators import ValidationError

from ..widgets import SelectWidget
from .select import SelectField


def get_pk_from_identity(obj):
    cls, key = identity_key(instance=obj)
    return ':'.join(six.text_type(x) for x in key)


class GroupedQuerySelectField(SelectField):
    widget = SelectWidget()

    def __init__(
        self,
        label=None,
        validators=None,
        query_factory=None,
        get_pk=None,
        get_label=None,
        get_group=None,
        allow_blank=False,
        blank_text='',
        blank_value='__None',
        **kwargs
    ):
        super(GroupedQuerySelectField, self).__init__(
            label,
            validators,
            coerce=lambda x: x,
            **kwargs
        )

        self.query = None
        self.query_factory = query_factory

        if get_pk is None:
            self.get_pk = get_pk_from_identity
        else:
            self.get_pk = get_pk

        self.get_label = get_label
        self.get_group = get_group

        self.allow_blank = allow_blank
        self.blank_text = blank_text
        self.blank_value = blank_value

        self._choices = None

    def _get_object_list(self):
        query = self.query or self.query_factory()
        return list((six.text_type(self.get_pk(obj)), obj) for obj in query)

    def _pre_process_object_list(self, object_list):
        return sorted(
            object_list,
            key=lambda x: (x[1] or u'', self.get_label(x[2]) or u'')
        )

    @property
    def choices(self):
        if not self._choices:
            object_list = map(
                lambda x: (x[0], self.get_group(x[1]), x[1]),
                self._get_object_list()
            )
            # object_list is (key, group, value) tuple
            choices = [
                (self.blank_value, self.blank_text)
            ] if self.allow_blank else []
            object_list = self._pre_process_object_list(object_list)
            for group, data in groupby(object_list, key=lambda x: x[1]):
                if group is not None:
                    group_items = []
                    for key, _, value in data:
                        group_items.append((key, self.get_label(value)))
                    choices.append((group, group_items))
                else:
                    for key, group, value in data:
                        choices.append((key, self.get_label(value)))
            self._choices = choices
        return self._choices

    @choices.setter
    def choices(self, value):
        pass

    @property
    def data(self):
        if self._formdata is not None:
            for pk, obj in self._get_object_list():
                if pk == self._formdata:
                    self.data = obj
                    break
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self._formdata = None

    def iter_choices(self):
        """
        We should update how choices are iter to make sure that value from
        internal list or tuple should be selected.
        """
        for value, label in self.concrete_choices:
            yield (
                value,
                label,
                (
                    self.coerce,
                    self.get_pk(self.data) if self.data else self.blank_value
                )
            )

    def process_formdata(self, valuelist):
        if valuelist:
            if self.allow_blank and valuelist[0] == self.blank_value:
                self.data = None
            else:
                self._data = None
                self._formdata = valuelist[0]

    def pre_validate(self, form):
        data = self.data
        if data is not None:
            for pk, obj in self._get_object_list():
                if data == obj:
                    break
            else:
                raise ValidationError('Not a valid choice')
        elif self._formdata or not self.allow_blank:
            raise ValidationError('Not a valid choice')
