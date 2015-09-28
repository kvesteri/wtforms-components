from wtforms import Form
from wtforms_test import FormTestCase

from tests import MultiDict
from wtforms_components import FloatIntervalField, IntIntervalField


class RangeFieldTestCase(FormTestCase):
    def init_form(self, **kwargs):
        class TestForm(Form):
            interval = self.interval_field(**kwargs)

        self.form_class = TestForm
        return self.form_class

    def test_valid_intervals(self):
        form_class = self.init_form()
        for interval in self.valid_ranges:
            form = form_class(MultiDict(interval=interval))
            form.validate()
            assert len(form.errors) == 0

    def test_invalid_intervals(self):
        form_class = self.init_form()
        for interval in self.invalid_ranges:
            form = form_class(MultiDict(interval=interval))
            form.validate()
            assert len(form.errors['interval']) == 1

    def test_field_rendering_when_validation_fails(self):
        form_class = self.init_form()
        form = form_class(MultiDict(interval='invalid'))
        form.validate()
        assert 'value="invalid"' in str(form.interval)

    def test_converts_empty_strings_to_none(self):
        form_class = self.init_form()
        form = form_class(MultiDict(interval=''))
        assert form.data == {'interval': None}


class TestIntIntervalField(RangeFieldTestCase):
    def setup_method(self, method):
        self.valid_ranges = [
            '13 - 14',
            '13 - 13',
            '0 - 99',
            '88'
        ]
        self.invalid_ranges = [
            'abc',
            '14 - 13',
        ]
        self.interval_field = IntIntervalField


class TestFloatIntervalField(RangeFieldTestCase):
    def setup_method(self, method):
        self.valid_ranges = [
            '13 - 14',
            '13 - 13',
            '0 - 99',
            '88'
        ]
        self.invalid_ranges = [
            'abc',
            '14 - 13',
        ]
        self.interval_field = FloatIntervalField
