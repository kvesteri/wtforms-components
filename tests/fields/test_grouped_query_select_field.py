import sqlalchemy as sa
from wtforms import Form

from tests import DatabaseTestCase, MultiDict
from wtforms_components import GroupedQuerySelectField


class TestGroupedQuerySelectField(DatabaseTestCase):
    def create_models(self):
        class City(self.base):
            __tablename__ = 'city'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.String)
            country = sa.Column(sa.String)

        self.City = City

    def create_cities(self):
        self.session.add_all([
            self.City(name='Helsinki', country='Finland'),
            self.City(name='Vantaa', country='Finland'),
            self.City(name='New York', country='USA'),
            self.City(name='Washington', country='USA'),
            self.City(name='Stockholm', country='Sweden'),
        ])

    def create_form(self, **kwargs):
        query = self.session.query(self.City).order_by('name', 'country')

        class MyForm(Form):
            city = GroupedQuerySelectField(
                label=kwargs.get('label', 'City'),
                query_factory=kwargs.get('query_factory', lambda: query),
                get_label=kwargs.get('get_label', lambda c: c.name),
                get_group=kwargs.get('get_group', lambda c: c.country),
                allow_blank=kwargs.get('allow_blank', False),
                blank_text=kwargs.get('blank_text', ''),
                blank_value=kwargs.get('blank_value', '__None'),
            )

        return MyForm

    def test_rendering(self):
        MyForm = self.create_form()
        self.create_cities()
        assert str(MyForm().city).replace('\n', '') == (
            '<select id="city" name="city">'
            '<optgroup label="Finland">'
            '<option value="1">Helsinki</option>'
            '<option value="2">Vantaa</option>'
            '</optgroup><optgroup label="Sweden">'
            '<option value="5">Stockholm</option>'
            '</optgroup>'
            '<optgroup label="USA">'
            '<option value="3">New York</option>'
            '<option value="4">Washington</option>'
            '</optgroup>'
            '</select>'
        )

    def test_custom_none_value(self):
        self.create_cities()
        MyForm = self.create_form(
            allow_blank=True,
            blank_text='Choose city...',
            blank_value=''
        )
        form = MyForm(MultiDict({'city': ''}))
        assert form.validate(), form.errors
        assert '<option selected value="">Choose city...</option>' in (
            str(form.city)
        )
