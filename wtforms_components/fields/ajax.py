# -*- coding: utf-8 -*-
import operator

import six
from wtforms import fields, widgets
from wtforms.validators import ValidationError

anyjson = None
try:
    import anyjson
except ImportError:
    pass


class ImproperlyConfigured(Exception):
    pass


class AjaxField(fields.Field):
    widget = widgets.HiddenInput()

    def __init__(
        self,
        label=None,
        validators=None,
        data_url=None,
        get_object=None,
        get_pk=None,
        coerce=int,
        get_label=None,
        allow_blank=False,
        blank_text='',
        **kwargs
    ):
        super(AjaxField, self).__init__(label, validators, **kwargs)

        if anyjson is None:
            raise ImproperlyConfigured(
                'AjaxField requires anyjson extension to be installed.'
            )

        if data_url is None:
            raise Exception('data_url must be given')

        self.get_pk = get_pk

        if get_label is None:
            self.get_label = lambda x: x
        elif isinstance(get_label, six.string_types):
            self.get_label = operator.attrgetter(get_label)
        else:
            self.get_label = get_label

        self.coerce = coerce
        self.data_url = data_url
        self.get_object = get_object
        self.allow_blank = allow_blank
        self.blank_text = blank_text

    @property
    def data(self):
        if self._formdata is not None:
            try:
                pk = self.coerce(self._formdata)
            except ValueError:
                self.data = None
            else:
                self.data = self.get_object(pk)
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self._formdata = None

    def process_formdata(self, valuelist):
        if valuelist:
            if self.allow_blank and not valuelist[0]:
                self.data = None
            else:
                self._data = None
                self._formdata = valuelist[0]

    def pre_validate(self, form):
        if self.data is None:
            if self._formdata or not self.allow_blank:
                raise ValidationError('Not a valid choice')

    def __call__(self, **kwargs):
        kwargs.setdefault(
            'data-allow-clear', anyjson.serialize(self.allow_blank)
        )
        kwargs.setdefault('data-placeholder', self.blank_text)
        kwargs.setdefault('data-url', self.data_url)
        if self.data is not None:
            kwargs.setdefault('data-initial-label', self.get_label(self.data))
            kwargs.setdefault('value', self.get_pk(self.data))
        else:
            kwargs.setdefault('value', '')
        return super(AjaxField, self).__call__(**kwargs)
