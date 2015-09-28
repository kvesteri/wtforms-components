from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from wtforms import Form
from wtforms.validators import DataRequired
from wtforms_test import FormTestCase


class MultiDict(dict):
    def getlist(self, key):
        return [self[key]]


class DatabaseTestCase(FormTestCase):
    def setup_method(self, method):
        self.engine = create_engine('sqlite:///:memory:')

        self.base = declarative_base()
        self.create_models()

        self.base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def teardown_method(self, method):
        self.session.close_all()
        self.base.metadata.drop_all(self.engine)
        self.engine.dispose()


class SimpleFieldTestCase(FormTestCase):
    field_class = None

    def init_form(self, **kwargs):
        class TestForm(Form):
            test_field = self.field_class(**kwargs)

        self.form_class = TestForm
        return self.form_class


class FieldTestCase(SimpleFieldTestCase):
    def test_assigns_required_from_validator(self):
        form_class = self.init_form(
            validators=[DataRequired()]
        )
        form = form_class()
        assert (
            '<input id="test_field"'
            ' name="test_field" required'
        ) in str(form.test_field)

    def test_renders_autofocus(self):
        form_class = self.init_form(
            widget=self.field_class.widget.__class__(
                autofocus=True
            )
        )
        form = form_class()
        assert 'autofocus' in str(form.test_field)

    def test_renders_required(self):
        form_class = self.init_form(
            widget=self.field_class.widget.__class__(
                required=True
            )
        )
        form = form_class()
        assert 'required' in str(form.test_field)

    def test_renders_disabled(self):
        form_class = self.init_form(
            widget=self.field_class.widget.__class__(
                disabled=True
            )
        )
        form = form_class()
        assert 'disabled' in str(form.test_field)

    def test_renders_readonly(self):
        form_class = self.init_form(
            widget=self.field_class.widget.__class__(
                readonly=True
            )
        )
        form = form_class()
        assert 'readonly' in str(form.test_field)
