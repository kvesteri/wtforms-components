from wtforms import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired
from wtforms_test import FormTestCase

from tests import MultiDict
from wtforms_components import If


class TestIfValidator(FormTestCase):
    def test_only_validates_if_condition_returns_true(self):
        class MyForm(Form):
            name = StringField(
                validators=[
                    If(
                        lambda form, field: False,
                        DataRequired(),
                    )
                ]
            )

        form = MyForm(MultiDict({"name": ""}))
        form.validate()
        assert not form.errors

    def test_encapsulates_given_validator(self):
        class MyForm(Form):
            name = StringField(
                validators=[
                    If(
                        lambda form, field: True,
                        DataRequired(),
                    )
                ]
            )

        form = MyForm(MultiDict({"name": ""}))
        form.validate()
        assert "name" in form.errors

    def test_supports_custom_error_messages(self):
        class MyForm(Form):
            name = StringField(
                validators=[
                    If(
                        lambda form, field: True,
                        DataRequired(),
                        message="Validation failed.",
                    )
                ]
            )

        form = MyForm(MultiDict({"name": ""}))
        form.validate()
        assert form.errors["name"] == ["Validation failed."]
