from datetime import time

from wtforms import Form
from wtforms_test import FormTestCase

from tests import MultiDict
from wtforms_components import TimeField, TimeRange


class TestTimeRangeValidator(FormTestCase):
    def init_form(self, **kwargs):
        class ModelTestForm(Form):
            time = TimeField(validators=[TimeRange(**kwargs)])

        self.form_class = ModelTestForm
        return self.form_class

    def test_time_greater_than_validator(self):
        form_class = self.init_form(min=time(12))
        form = form_class(MultiDict(time='11:12'))
        form.validate()
        error_msg = u'Time must be greater than 12:00.'
        assert form.errors['time'] == [error_msg]

    def test_time_less_than_validator(self):
        form_class = self.init_form(max=time(13, 30))
        form = form_class(MultiDict(time='13:40'))
        form.validate()
        error_msg = u'Time must be less than 13:30.'
        assert form.errors['time'] == [error_msg]

    def test_time_between_validator(self):
        form_class = self.init_form(min=time(12), max=time(13))
        form = form_class(MultiDict(time='14:30'))
        form.validate()
        error_msg = u'Time must be between 12:00 and 13:00.'
        assert form.errors['time'] == [error_msg]
