from wtforms import Form
from wtforms.fields import TextField
from wtforms_test import FormTestCase

from tests import MultiDict
from wtforms_components import read_only


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

    def test_prevents_value_population(self):
        class MyForm(Form):
            name = TextField()

        class MyModel(object):
            pass

        form = MyForm()
        model = MyModel()
        form.name.data = 'Existing value'
        read_only(form.name)
        form.populate_obj(model)
        assert not hasattr(model, 'name')
