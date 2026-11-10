from wtforms import Form
from wtforms_test import FormTestCase

from tests import MultiDict
from wtforms_components import SelectField


class Dummy:
    fruits = []


class TestSelectField(FormTestCase):
    choices = (
        ("Fruits", (("apple", "Apple"), ("peach", "Peach"), ("pear", "Pear"))),
        (
            "Vegetables",
            (
                ("cucumber", "Cucumber"),
                ("potato", "Potato"),
                ("tomato", "Tomato"),
            ),
        ),
    )

    def init_form(self, **kwargs):
        class TestForm(Form):
            fruit = SelectField(**kwargs)

        self.form_class = TestForm
        return self.form_class

    def test_understands_nested_choices(self):
        form_class = self.init_form(choices=self.choices)
        form = form_class(MultiDict([("fruit", "invalid")]))
        form.validate()

        assert len(form.errors["fruit"]) == 1

    def test_understands_mixing_of_choice_types(self):
        choices = (
            ("Fruits", (("apple", "Apple"), ("peach", "Peach"), ("pear", "Pear"))),
            ("cucumber", "Cucumber"),
        )

        form_class = self.init_form(choices=choices)
        form = form_class(MultiDict([("fruit", "cucumber")]))
        form.validate()
        assert len(form.errors) == 0

    def test_renders_optgroups_mixed_with_ungrouped_options(self):
        choices = (
            ("none", "None"),
            ("Fruits", (("apple", "Apple"), ("pear", "Pear"))),
            ("cucumber", "Cucumber"),
        )
        form = self.init_form(choices=choices, default="pear")()
        assert str(form.fruit) == (
            '<select id="fruit" name="fruit">'
            '<option value="none">None</option>'
            '<optgroup label="Fruits">'
            '<option value="apple">Apple</option>'
            '<option selected value="pear">Pear</option>'
            "</optgroup>"
            '<option value="cucumber">Cucumber</option>'
            "</select>"
        )

    def test_accepts_iterator_as_choices(self):
        form_class = self.init_form(choices=zip(["apple", "pear"], ["Apple", "Pear"]))
        form = form_class(MultiDict([("fruit", "pear")]))
        assert '<option selected value="pear">Pear</option>' in str(form.fruit)
        assert form.validate()

    def test_validates_without_coercing_choices(self):
        form_class = self.init_form(choices=[("", "---"), (1, "One")], coerce=int)
        form = form_class(MultiDict([("fruit", "1")]))
        assert form.validate()

    def test_understands_callables_as_choices(self):
        form_class = self.init_form(choices=lambda: [])
        form = form_class(MultiDict([("fruit", "invalid")]))
        form.validate()

        assert len(form.errors["fruit"]) == 1

    def test_option_selected(self):
        form_class = self.init_form(choices=self.choices)

        obj = Dummy()
        obj.fruit = "peach"
        form = form_class(obj=obj)
        assert '<option selected value="peach">Peach</option>' in str(form.fruit)

    def test_nested_option_selected_by_field_default_value(self):
        form_class = self.init_form(choices=self.choices, default="pear")
        form = form_class()
        assert '<option selected value="pear">Pear</option>' in str(form.fruit)

    def test_option_selected_by_field_default_value(self):
        choices = [("apple", "Apple"), ("peach", "Peach"), ("pear", "Pear")]
        form_class = self.init_form(choices=choices, default="pear")
        form = form_class()
        assert '<option selected value="pear">Pear</option>' in str(form.fruit)

    def test_callable_option_selected_by_field_default_value(self):
        def choices():
            return [("apple", "Apple"), ("peach", "Peach"), ("pear", "Pear")]

        form_class = self.init_form(choices=choices, default="pear")
        form = form_class()
        assert '<option selected value="pear">Pear</option>' in str(form.fruit)

    def test_data_coercion(self):
        choices = (
            ("Fruits", ((0, "Apple"), (1, "Peach"), (2, "Pear"))),
            (3, "Cucumber"),
        )

        form_class = self.init_form(choices=choices, coerce=int)
        form = form_class(MultiDict([("fruit", "1")]))
        form.validate()
        assert not form.errors
