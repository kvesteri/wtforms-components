from wtforms.validators import NumberRange

from tests import FieldTestCase, MultiDict
from wtforms_components import DecimalField
from wtforms_components.widgets import NumberInput


class TestDecimalField(FieldTestCase):
    field_class = DecimalField

    def test_assigns_min_and_max(self):
        form_class = self.init_form(
            validators=[NumberRange(min=2, max=10)]
        )
        form = form_class(MultiDict(test_field=3))
        assert str(form.test_field) == (
            '<input id="test_field" max="10" min="2" '
            'name="test_field" step="any" type="number" value="3">'
        )

    def test_assigns_step(self):
        form_class = self.init_form(
            widget=NumberInput(step='0.1')
        )
        form = form_class(MultiDict(test_field=3))
        assert str(form.test_field) == (
            '<input id="test_field" '
            'name="test_field" step="0.1" type="number" value="3">'
        )
