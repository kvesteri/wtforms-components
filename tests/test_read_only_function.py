from wtforms_components import read_only
from wtforms_test import FormTestCase
from wtforms import Form
from wtforms.fields import TextField
from tests import MultiDict


class TestReadOnlyFunction(FormTestCase):
    def test_prevents_value_changing(self):
        class MyForm(Form):
            name = TextField(default='')

        form = MyForm()
        read_only(form.name)
        form.process(MultiDict({'name': 'New value'}))
        assert form.name.data == ''

    def test_preserves_previous_value(self):
        class MyForm(Form):
            name = TextField()

        form = MyForm()
        form.name.data = 'Previous value'
        read_only(form.name)
        form.process(MultiDict({'name': 'New value'}))
        assert form.name.data == 'Previous value'
