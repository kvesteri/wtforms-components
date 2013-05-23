from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from wtforms_test import FormTestCase
from wtforms import Form
from wtforms.validators import DataRequired


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


class FieldTestCase(FormTestCase):
    """Test case for form field types."""

    field_class = None

    def init_form(self, **kwargs):
        class TestForm(Form):
            test_field = self.field_class(**kwargs)

        self.form_class = TestForm
        return self.form_class

    def test_assigns_required(self):
        form_class = self.init_form(
            validators=[DataRequired()]
        )
        form = form_class()
        assert (
            '<input id="test_field"'
            ' name="test_field" required'
        ) in str(form.test_field)
