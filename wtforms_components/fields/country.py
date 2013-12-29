import operator
from .select import SelectField
from sqlalchemy_utils.types import Country
from sqlalchemy_utils import i18n


class CountryField(SelectField):
    def __init__(self, *args, **kwargs):
        kwargs['coerce'] = Country
        super(CountryField, self).__init__(*args, **kwargs)
        self.choices = self._get_choices

    def _get_choices(self):
        # Get all territories and filter out continents (3-digit code)
        # and some odd territories such as "Unknown or Invalid Region"
        # ("ZZ"), "European Union" ("QU") and "Outlying Oceania" ("QO").
        territories = [
            (code, name)
            for code, name in i18n.get_locale().territories.iteritems()
            if len(code) == 2 and code not in ('QO', 'QU', 'ZZ')
        ]
        return sorted(territories, key=operator.itemgetter(1))
