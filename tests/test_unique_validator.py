from pytest import raises
import sqlalchemy as sa

from wtforms_components import ModelForm, Unique
from wtforms.fields import TextField
from tests import MultiDict, DatabaseTestCase


class TestUniqueValidator(DatabaseTestCase):
    def create_models(self):
        class User(self.base):
            __tablename__ = 'event'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255), unique=True)

        self.User = User

    def test_raises_exception_if_improperly_configured(self):
        with raises(Exception):
            class MyForm(ModelForm):
                name = TextField(
                    validators=[Unique(
                        self.User.name,
                    )]
                )

    def test_existing_name_collision(self):
        class MyForm(ModelForm):
            name = TextField(
                validators=[Unique(
                    self.User.name,
                    get_session=lambda: self.session
                )]
            )

        self.session.add(self.User(name=u'someone'))
        self.session.commit()

        form = MyForm(MultiDict({'name': u'someone'}))
        form.validate()
        assert form.errors == {'name': [u'Already exists.']}

    def test_without_obj_without_collision(self):
        class MyForm(ModelForm):
            name = TextField(
                validators=[Unique(
                    self.User.name,
                    get_session=lambda: self.session
                )]
            )

        self.session.add(self.User(name=u'someone else'))
        self.session.commit()

        form = MyForm(MultiDict({'name': u'someone'}))
        assert form.validate()

    def test_existing_name_no_collision(self):
        class MyForm(ModelForm):
            name = TextField(
                validators=[Unique(
                    self.User.name,
                    get_session=lambda: self.session
                )]
            )

        obj = self.User(name=u'someone')
        self.session.add(obj)

        form = MyForm(MultiDict({'name': u'someone'}), obj=obj)
        assert form.validate()

    def test_supports_model_query_parameter(self):
        self.User.query = self.session.query(self.User)

        class MyForm(ModelForm):
            name = TextField(
                validators=[Unique(
                    self.User.name,
                )]
            )

        form = MyForm(MultiDict({'name': u'someone'}))
        assert form.validate()
