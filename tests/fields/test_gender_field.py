import pytest
from wtforms import Form
from wtforms_test import FormTestCase

from tests import MultiDict
from wtforms_components import GenderField


def test_no_value():
    class TestForm(Form):
        gender = GenderField()

    form = TestForm()
    gender_html = form.gender()
    expected_html = (
        '<select id="gender" name="gender">'
            '<option value="">Not Specified</option>'
            '<option value="male">Male</option>'
            '<option value="female">Female</option>'
            '<option data-render-as-text value="non-binary">Non-binary</option>'
        '</select>'
    )
    assert gender_html == expected_html


def test_male_value():
    class TestForm(Form):
        gender = GenderField()

    values = MultiDict(gender='male')

    form = TestForm(values)
    gender_html = form.gender()
    expected_html = (
        '<select id="gender" name="gender">'
            '<option value="">Not Specified</option>'
            '<option selected value="male">Male</option>'
            '<option value="female">Female</option>'
            '<option data-render-as-text value="non-binary">Non-binary</option>'
        '</select>'
    )
    assert gender_html == expected_html


def test_female_value():
    class TestForm(Form):
        gender = GenderField()

    values = MultiDict(gender='female')

    form = TestForm(values)
    gender_html = form.gender()
    expected_html = (
        '<select id="gender" name="gender">'
            '<option value="">Not Specified</option>'
            '<option value="male">Male</option>'
            '<option selected value="female">Female</option>'
            '<option data-render-as-text value="non-binary">Non-binary</option>'
        '</select>'
    )
    assert gender_html == expected_html


def test_non_binary_value():
    class TestForm(Form):
        gender = GenderField()

    values = MultiDict(gender='non-binary')

    form = TestForm(values)
    gender_html = form.gender()
    expected_html = (
        '<input id="gender" name="gender" type="text" value="non-binary">'
    )
    assert gender_html == expected_html


def test_non_simple_value():
    class TestForm(Form):
        gender = GenderField()

    values = MultiDict(gender='transgender')

    form = TestForm(values)
    gender_html = form.gender()
    expected_html = (
        '<input id="gender" name="gender" type="text" value="transgender">'
    )
    assert gender_html == expected_html


def test_customizable_simple_values():
    simple_genders = (
        ('', "Not Specified"),
        ('female', "Female"),
        ('male', "Male"),
        ('trans', "Transgender"),
        ('non-binary', "Custom"),
    )

    class TestForm(Form):
        gender = GenderField(simple_genders=simple_genders)

    form = TestForm()
    gender_html = form.gender()
    expected_html = (
        '<select id="gender" name="gender">'
            '<option value="">Not Specified</option>'
            '<option value="female">Female</option>'
            '<option value="male">Male</option>'
            '<option value="trans">Transgender</option>'
            '<option data-render-as-text value="non-binary">Custom</option>'
        '</select>'
    )
    assert gender_html == expected_html


def test_customizable_simple_value_selected():
    simple_genders = (
        ('', "Not Specified"),
        ('female', "Female"),
        ('male', "Male"),
        ('trans', "Transgender"),
        ('non-binary', "Custom"),
    )

    class TestForm(Form):
        gender = GenderField(simple_genders=simple_genders)

    values = MultiDict(gender='trans')

    form = TestForm(values)
    gender_html = form.gender()
    expected_html = (
        '<select id="gender" name="gender">'
            '<option value="">Not Specified</option>'
            '<option value="female">Female</option>'
            '<option value="male">Male</option>'
            '<option selected value="trans">Transgender</option>'
            '<option data-render-as-text value="non-binary">Custom</option>'
        '</select>'
    )
    assert gender_html == expected_html


def test_customized_non_simple_value():
    simple_genders = (
        ('', "Not Specified"),
        ('female', "Female"),
        ('male', "Male"),
        ('trans', "Transgender"),
        ('non-binary', "Custom"),
    )

    class TestForm(Form):
        gender = GenderField(simple_genders=simple_genders)

    values = MultiDict(gender='genderfluid')

    form = TestForm(values)
    gender_html = form.gender()
    expected_html = (
        '<input id="gender" name="gender" type="text" value="genderfluid">'
    )
    assert gender_html == expected_html
