from wtforms_components import NumberRangeField
from wtforms_test import FormTestCase
from wtforms import Form
from tests import MultiDict


class TestNumberRangeField(FormTestCase):
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

    def init_form(self, **kwargs):
        class TestForm(Form):
            number_range = NumberRangeField(**kwargs)

        self.form_class = TestForm
        return self.form_class

    def test_valid_number_ranges(self):
        form_class = self.init_form()
        for number_range in self.valid_ranges:
            form = form_class(MultiDict(number_range=number_range))
            form.validate()
            assert len(form.errors) == 0

    def test_invalid_number_ranges(self):
        form_class = self.init_form()
        for number_range in self.invalid_ranges:
            form = form_class(MultiDict(number_range=number_range))
            form.validate()
            assert len(form.errors['number_range']) == 1

    def test_field_rendering_when_validation_fails(self):
        form_class = self.init_form()
        form = form_class(MultiDict(number_range='invalid'))
        form.validate()
        assert 'value="invalid"' in str(form.number_range)

    def test_converts_empty_strings_to_none(self):
        form_class = self.init_form()
        form = form_class(MultiDict(number_range=''))
        assert form.data == {'number_range': None}
