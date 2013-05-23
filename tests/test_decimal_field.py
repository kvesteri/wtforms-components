from wtforms_components import DecimalField
from wtforms_test import FormTestCase
from wtforms import Form
from wtforms.validators import NumberRange
from tests import MultiDict


class TestDecimalField(FormTestCase):
    def init_form(self, **kwargs):
        class TestForm(Form):
            test_field = DecimalField(**kwargs)

        self.form_class = TestForm
        return self.form_class

    def test_assigns_min_and_max(self):
        form_class = self.init_form(
            validators=[NumberRange(min=2, max=10)]
        )
        form = form_class(MultiDict(test_field=3))
        assert str(form.test_field) == (
            '<input id="test_field" max="10" min="2" '
            'name="test_field" type="number" value="3">'
        )
