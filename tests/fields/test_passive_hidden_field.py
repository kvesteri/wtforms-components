from wtforms import Form
from wtforms_test import FormTestCase

from tests import MultiDict
from wtforms_components import PassiveHiddenField


class TestPassiveHiddenField(FormTestCase):
    def test_does_not_populate_obj_values(self):
        class MyForm(Form):
            id = PassiveHiddenField()

        class A(object):
            id = None

        form = MyForm(MultiDict({'id': 12}))
        a = A()
        form.populate_obj(a)
        assert a.id is None
