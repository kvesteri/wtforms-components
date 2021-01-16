from wtforms import Form
from wtforms.validators import DataRequired, Email
from wtforms_test import FormTestCase

from tests import MultiDict
from wtforms_components import Chain

try:
    from wtforms.fields import TextField
except ImportError:  # wtforms3
    from wtforms.fields import StringField as TextField


class TestChainValidator(FormTestCase):
    def test_validates_whole_chain(self):
        class MyForm(Form):
            email = TextField(validators=[Chain([DataRequired(), Email()])])

        form = MyForm(MultiDict({'name': ''}))
        form.validate()
        assert 'email' in form.errors
