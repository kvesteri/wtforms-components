import pytest
from wtforms.validators import ValidationError

from wtforms_components import Email


class DummyTranslations:
    def gettext(self, string):
        return string

    def ngettext(self, singular, plural, n):
        if n == 1:
            return singular

        return plural


class DummyForm(dict):
    pass


class DummyField:
    _translations = DummyTranslations()

    def __init__(self, data, errors=(), raw_data=None):
        self.data = data
        self.errors = list(errors)
        self.raw_data = raw_data

    def gettext(self, string):
        return self._translations.gettext(string)

    def ngettext(self, singular, plural, n):
        return self._translations.ngettext(singular, plural, n)


class TestEmailValidator:
    def setup_method(self, method):
        self.form = DummyForm()

    @pytest.mark.parametrize(
        "email",
        [
            "email@here.com",
            "weirder-email@here.and.there.com",
            "example@valid-----hyphens.com",
            "example@valid-with-hyphens.com",
            "test@domain.with.idn.tld.उदाहरण.परीक्षा",
            '"\\\011"@here.com',
        ],
    )
    def test_returns_none_on_valid_email(self, email):
        validate_email = Email()
        validate_email(self.form, DummyField(email))

    @pytest.mark.parametrize(
        ("email",),
        [
            (None,),
            ("",),
            ("abc",),
            ("abc@",),
            ("abc@bar",),
            ("a @x.cz",),
            ("abc@.com",),
            ("something@@somewhere.com",),
            ("email@127.0.0.1",),
            ("example@invalid-.com",),
            ("example@-invalid.com",),
            ("example@inv-.alid-.com",),
            ("example@inv-.-alid.com",),
            # Quoted-string format (CR not allowed)
            ('"\\\012"@here.com',),
        ],
    )
    def test_raises_validationerror_on_invalid_email(self, email):
        validate_email = Email()
        with pytest.raises(ValidationError):
            validate_email(self.form, DummyField(email))

    def test_default_validation_error_message(self):
        validate_email = Email()
        try:
            validate_email(self.form, DummyField("@@@"))
            assert False, "No validation error thrown."
        except ValidationError as e:
            assert str(e) == "Invalid email address."
