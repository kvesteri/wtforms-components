from datetime import time

from tests import FieldTestCase, MultiDict
from wtforms_components import TimeField, TimeRange


class TestTimeField(FieldTestCase):
    field_class = TimeField

    def setup_method(self, method):
        self.valid_times = [
            '00:00',
            '11:11',
            '12:15'
        ]
        self.invalid_times = [
            '00:61',
            '25:01',
            'unknown',
        ]

    def test_valid_times(self):
        form_class = self.init_form()
        for time_ in self.valid_times:
            form = form_class(MultiDict(test_field=time_))
            form.validate()
            assert len(form.errors) == 0

    def test_invalid_times(self):
        form_class = self.init_form()
        for time_ in self.invalid_times:
            form = form_class(MultiDict(test_field=time_))
            form.validate()
            assert len(form.errors['test_field']) == 1

    def test_assigns_min_and_max(self):
        form_class = self.init_form(
            validators=[TimeRange(
                min=time(12, 12),
                max=time(13, 30)
            )]
        )
        form = form_class(MultiDict(test_field='13:20'))
        assert str(form.test_field) == (
            '<input id="test_field" max="13:30:00" min="12:12:00"'
            ' name="test_field" type="time" value="13:20">'
        )

    def test_renders_input_time_at_midnight(self):
        form_class = self.init_form()
        form = form_class(MultiDict(test_field='00:00'))
        assert str(form.test_field) == (
            '<input id="test_field" name="test_field"'
            ' type="time" value="00:00">'
        )
