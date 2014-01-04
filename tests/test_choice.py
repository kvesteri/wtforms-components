from pytest import mark
from wtforms_components.fields.select import Choice, Choices


def test_choice_init_with_all_args():
    choice = Choice('1', 'Choice 1', 1)
    assert choice.key == '1'
    assert choice.label == 'Choice 1'
    assert choice.value == 1


def test_choice_init_with_single_arg():
    choice = Choice('1')
    assert choice.key == '1'
    assert choice.label == '1'
    assert choice.value == '1'


def test_choice_repr():
    choice = Choice('1')
    assert repr(choice) == "Choice(key='1', label='1', value='1')"


def test_add_operator_with_another_choice():
    choices = Choice('1') + Choice('2')
    assert isinstance(choices, Choices)


def test_choices_length():
    assert len(Choices(['1'])) == 1


def test_add_operator_with_choice():
    assert len(Choices(['1']) + Choice('2')) == 2
