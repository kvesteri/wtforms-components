from datetime import datetime

from tests import FieldTestCase, MultiDict
from wtforms_components import DateRange, DateTimeField


class TestDateTimeField(FieldTestCase):
    field_class = DateTimeField

    def test_assigns_min_and_max(self):
        form_class = self.init_form(
            validators=[DateRange(
                min=datetime(2000, 1, 1),
                max=datetime(2000, 10, 10)
            )]
        )
        form = form_class(MultiDict(test_field='2000-2-2'))
        assert str(form.test_field) == (
            '<input id="test_field" max="2000-10-10T00:00:00Z" '
            'min="2000-01-01T00:00:00Z"'
            ' name="test_field" type="datetime" value="2000-2-2">'
        )
