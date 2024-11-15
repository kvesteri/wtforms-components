from tests import MultiDict, SimpleFieldTestCase
from wtforms_components import JSONField


class TestJSONField(SimpleFieldTestCase):
    field_class = JSONField

    def setup_method(self, method):
        self.valid_jsons = [
            '{"a": {"b": true, "c": "lv", "d": 3}, "e": {"f": {"g": [85]}}}'
        ]
        self.invalid_jsons = [
            '{"a": {"b": bzz, "c": "lv", "d": 3}, "e": {"f": {"g": [85]}}}'
        ]

    def test_valid_times(self):
        form_class = self.init_form()
        for time_ in self.valid_jsons:
            form = form_class(MultiDict(test_field=time_))
            form.validate()
            assert len(form.errors) == 0

    def test_invalid_times(self):
        form_class = self.init_form()
        for time_ in self.invalid_jsons:
            form = form_class(MultiDict(test_field=time_))
            form.validate()
            assert len(form.errors["test_field"]) == 1
