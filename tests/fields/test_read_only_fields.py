from wtforms.fields import BooleanField

from tests import MultiDict, SimpleFieldTestCase
from wtforms_components import read_only


class TestReadOnlyCheckboxField(SimpleFieldTestCase):
    field_class = BooleanField

    def test_has_readonly_and_disabled_attributes_in_html(self):
        form_class = self.init_form()
        form = form_class(MultiDict(test_field='y'))
        read_only(form.test_field)
        assert (
            '<input checked disabled id="test_field" '
            'name="test_field" readonly type="checkbox" value="y">'
        ) in str(form.test_field)
