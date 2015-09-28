from datetime import date, datetime, time

from wtforms import Form
from wtforms.validators import DataRequired

from tests import MultiDict, SimpleFieldTestCase
from wtforms_components.fields import SplitDateTimeField


class Obj(object):
    test_field = None


class TestSplitDateTimeField(SimpleFieldTestCase):
    field_class = SplitDateTimeField

    def test_assigns_required_to_date(self):
        form_class = self.init_form(datetime_form={
            'date': {'validators': [DataRequired()]}
        })
        form = form_class()
        assert str(form.test_field.date) == (
            '<input id="test_field-date" name="test_field-date" required '
            'type="date" value="">'
        )

    def test_renders_date_field(self):
        form_class = self.init_form()
        form = form_class()
        assert str(form.test_field.date) == (
            '<input id="test_field-date" name="test_field-date" type="date" '
            'value="">'
        )

    def test_assigns_required_to_time(self):
        form_class = self.init_form(datetime_form={
            'time': {'validators': [DataRequired()]}
        })
        form = form_class()
        assert str(form.test_field.time) == (
            '<input id="test_field-time" name="test_field-time" required '
            'type="time" value="">'
        )

    def test_renders_time_field(self):
        form_class = self.init_form()
        form = form_class()
        assert str(form.test_field.time) == (
            '<input id="test_field-time" name="test_field-time" type="time" '
            'value="">'
        )

    def test_processes_values(self):
        form_class = self.init_form()
        form = form_class(MultiDict({
            'test_field-date': '2000-3-2',
            'test_field-time': '19:10',
        }))
        assert form.test_field.data['date'] == date(2000, 3, 2)
        assert form.test_field.data['time'] == time(19, 10)

    def test_populates_object(self):
        form_class = self.init_form()
        form = form_class(MultiDict({
            'test_field-date': '2000-3-2',
            'test_field-time': '19:10',
        }))
        obj = Obj()
        form.populate_obj(obj)
        assert obj.test_field == datetime(2000, 3, 2, 19, 10)

    def test_processes_values_when_format_is_set(self):
        form_class = self.init_form(datetime_form={
            'date': {'format': '%d.%m.%Y'},
            'time': {'format': '%H.%M'},
        })
        form = form_class(MultiDict({
            'test_field-date': '2.3.2000',
            'test_field-time': '19.10',
        }))
        assert form.test_field.data['date'] == date(2000, 3, 2)
        assert form.test_field.data['time'] == time(19, 10)

    def test_default_base_form(self):
        form_class = self.init_form()
        form = form_class()
        assert form.test_field.form.__class__.__bases__ == (Form,)

    def test_custom_base_form(self):
        class A(Form):
            pass
        form_class = self.init_form(datetime_form={'base_form': A})
        form = form_class()
        assert form.test_field.form.__class__.__bases__ == (A,)

    def test_custom_base_form_with_two_instances(self):
        class A(Form):
            pass
        form_class = self.init_form(datetime_form={'base_form': A})
        form = form_class()
        form2 = form_class()
        assert form.test_field.form.__class__.__bases__ == (A,)
        assert form2.test_field.form.__class__.__bases__ == (A,)
