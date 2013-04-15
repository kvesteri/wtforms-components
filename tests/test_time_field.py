from wtforms_components import TimeField
from wtforms_test import FormTestCase
from wtforms import Form
from tests import MultiDict


class TestPhoneNumberField(FormTestCase):
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

    def init_form(self, **kwargs):
        class TestForm(Form):
            time = TimeField(**kwargs)

        self.form_class = TestForm
        return self.form_class

    def test_valid_phone_numbers(self):
        form_class = self.init_form()
        for time in self.valid_times:
            form = form_class(MultiDict(time=time))
            form.validate()
            assert len(form.errors) == 0

    def test_invalid_phone_numbers(self):
        form_class = self.init_form()
        for time in self.invalid_times:
            form = form_class(MultiDict(time=time))
            form.validate()
            assert len(form.errors['time']) == 1
