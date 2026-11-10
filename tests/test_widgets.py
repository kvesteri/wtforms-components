from wtforms import Form
from wtforms.fields import SelectField
from wtforms_test import FormTestCase

from wtforms_components import SelectWidget


class Dummy:
    fruits = None


class TestSelectWidgetWithNativeSelect(FormTestCase):
    choices = ["apple", "peach", "pear", "cucumber", "potato", "tomato"]

    def init_form(self, **kwargs):
        class TestForm(Form):
            fruit = SelectField(widget=SelectWidget(), **kwargs)

        self.form_class = TestForm
        return self.form_class

    def test_option_selected(self):
        form_class = self.init_form(choices=self.choices)

        obj = Dummy()
        obj.fruit = "peach"
        form = form_class(obj=obj)
        assert '<option selected value="peach">peach</option>' in str(form.fruit)

    def test_default_value(self):
        form_class = self.init_form(choices=self.choices, default="pear")
        form = form_class()
        assert '<option selected value="pear">pear</option>' in str(form.fruit)

    def test_render_option_override(self):
        class CustomSelectWidget(SelectWidget):
            @classmethod
            def render_option(cls, value, label, selected, **kwargs):
                return f"<option>{label}!</option>"

        class TestForm(Form):
            fruit = SelectField(widget=CustomSelectWidget(), choices=["apple"])

        assert "<option>apple!</option>" in str(TestForm().fruit)
