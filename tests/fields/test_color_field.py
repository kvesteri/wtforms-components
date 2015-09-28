from wtforms import Form
from wtforms_test import FormTestCase

from tests import MultiDict
from wtforms_components import ColorField


class TestColorField(FormTestCase):
    def setup_method(self, method):
        self.valid_colors = [
            '#222222',
            'cyan',
        ]
        self.invalid_colors = [
            'abc',
            '#123123123',
        ]

    def init_form(self, **kwargs):
        class TestForm(Form):
            color = ColorField(**kwargs)

        self.form_class = TestForm
        return self.form_class

    def test_valid_colors(self):
        form_class = self.init_form()
        for color in self.valid_colors:
            form = form_class(MultiDict(color=color))
            form.validate()
            assert len(form.errors) == 0

    def test_invalid_number_ranges(self):
        form_class = self.init_form()
        for color in self.invalid_colors:
            form = form_class(MultiDict(color=color))
            form.validate()
            assert len(form.errors['color']) == 1

    def test_field_rendering_when_validation_fails(self):
        form_class = self.init_form()
        form = form_class(MultiDict(color='invalid'))
        form.validate()
        assert 'value="invalid"' in str(form.color)

    def test_converts_empty_strings_to_none(self):
        form_class = self.init_form()
        form = form_class(MultiDict(color=''))
        assert form.data == {'color': None}
