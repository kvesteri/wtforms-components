from pytest import mark
from wtforms_components.fields.select import Choice, Choices, ChoicesChain


class TestChoice(object):
    def test_init_with_all_args(self):
        choice = Choice('1', 'Choice 1', 1)
        assert choice.key == '1'
        assert choice.label == 'Choice 1'
        assert choice.value == 1

    def test_init_with_single_arg(self):
        choice = Choice('1')
        assert choice.key == '1'
        assert choice.label == '1'
        assert choice.value == '1'

    def test_repr(self):
        choice = Choice('1')
        assert repr(choice) == "Choice(key='1', label='1', value='1')"

    def test_add_operator_with_another_choice(self):
        choices = Choice('1') + Choice('2')
        assert isinstance(choices, Choices)

    def test_add_operator_with_choices(self):
        choices = Choices(['2'])
        first_choice = Choice('1')
        sum_choices = first_choice + choices
        assert choices != sum_choices
        assert len(sum_choices) == 2


class TestChoices(object):
    def test_choices_length(self):
        assert len(Choices(['1'])) == 1

    def test_add_operator_with_choice(self):
        assert len(Choices(['1']) + Choice('2')) == 2

    def test_add_operator_with_choices(self):
        sum_choices = Choices(['1']) + Choices(['2'])
        assert len(sum_choices) == 2
        assert isinstance(sum_choices, ChoicesChain)


class TestChoicesChain(object):
    def test_add_operator_with_choice(self):
        sum_choices = Choices(['1']) + Choices(['2']) + Choice('3')
        assert len(sum_choices) == 3

    def test_add_operator_with_choices(self):
        sum_choices = Choices(['1']) + Choices(['2']) + Choices(['3'])
        assert len(sum_choices) == 3

    def test_add_operator_with_choices_chain(self):
        sum_choices = Choices(['1']) + Choices(['2'])
        sum_choices2 = Choices(['3']) + Choices(['4'])
        assert len(sum_choices + sum_choices2) == 4

    def test_radd_operator_with_choice(self):
        sum_choices = Choice('3') + (Choices(['1']) + Choices(['2']))
        assert len(sum_choices) == 3

    def test_radd_operator_with_choices(self):
        sum_choices = Choices(['1']) + (Choices(['2']) + Choices(['3']))
        assert len(sum_choices) == 3
