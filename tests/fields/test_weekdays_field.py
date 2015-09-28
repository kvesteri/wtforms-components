from tests import MultiDict, SimpleFieldTestCase
from wtforms_components import WeekDaysField


class TestWeekDaysField(SimpleFieldTestCase):
    field_class = WeekDaysField

    def test_valid_weekdays(self):
        form_class = self.init_form()
        form = form_class(MultiDict(test_field=0))
        form.validate()
        assert len(form.errors) == 0

    def test_invalid_weekdays(self):
        form_class = self.init_form()
        form = form_class(MultiDict([
            ('test_field', '8'),
        ]))
        form.validate()
        assert len(form.errors['test_field']) == 1
