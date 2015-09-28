from sqlalchemy_utils.primitives import WeekDay, WeekDays
from wtforms.widgets import CheckboxInput, ListWidget

from .select_multiple import SelectMultipleField


class WeekDaysField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

    def __init__(self, *args, **kwargs):
        kwargs['coerce'] = lambda x: WeekDay(int(x))
        super(WeekDaysField, self).__init__(*args, **kwargs)
        self.choices = self._get_choices

    def _get_choices(self):
        days = WeekDays('1111111')
        for day in days:
            yield day.index, day.get_name(context='stand-alone')

    def process_data(self, value):
        self.data = WeekDays(value) if value else None

    def process_formdata(self, valuelist):
        self.data = WeekDays(self.coerce(x) for x in valuelist)

    def pre_validate(self, form):
        pass
