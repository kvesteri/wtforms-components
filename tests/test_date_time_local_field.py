from datetime import datetime
from wtforms_components import DateTimeLocalField, DateRange
from wtforms_test import FormTestCase
from wtforms import Form

from tests import MultiDict


class TestDateTimeLocalField(FormTestCase):
    def init_form(self, **kwargs):
        class TestForm(Form):
            test_field = DateTimeLocalField(**kwargs)

        self.form_class = TestForm
        return self.form_class

    def test_assigns_min_and_max(self):
        form_class = self.init_form(
            validators=[DateRange(
                min=datetime(2000, 1, 1),
                max=datetime(2000, 10, 10)
            )]
        )
        form = form_class(MultiDict(test_field='2000-2-2'))
        assert str(form.test_field) == (
            '<input id="test_field" max="2000-10-10 00:00:00" '
            'min="2000-01-01 00:00:00"'
            ' name="test_field" type="datetime-local" value="2000-2-2">'
        )
