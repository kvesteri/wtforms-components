Changelog
---------

Here you can see the full list of changes between each WTForms-Components
release.


0.10.3 (2017-03-03)
^^^^^^^^^^^^^^^^^^^

- Make SelectWidget backwards compatible (#52, pull request courtesy tvuotila)


0.10.2 (2016-12-05)
^^^^^^^^^^^^^^^^^^^

- Made read_only also add disabled attribute (#51, pull request courtesy quantus)


0.10.1 (2016-11-22)
^^^^^^^^^^^^^^^^^^^

- Added seconds support for TimeField (#48, pull request courtesy tvuotila)


0.10.0 (2016-01-28)
^^^^^^^^^^^^^^^^^^^

- Moved GroupedQuerySelectField to WTForms-Alchemy
- Moved PhoneNumber to WTForms-Alchemy
- Moved WeekdaysField to WTForms-Alchemy
- Moved Unique validator to WTForms-Alchemy
- Remove AJAXField dependency on SQLAlchemy-Utils
- Added PyPy support
- Fixed IntervalFields to work with intervals 0.6.0
- Updated intervals requirement to 0.6.0


0.9.9 (2016-01-10)
^^^^^^^^^^^^^^^^^^

- Added sane error handling with Unique validator when Form is missing `_obj` attribute (#34)


0.9.8 (2015-09-28)
^^^^^^^^^^^^^^^^^^

- Added isort and flake8 checks to ensure all code is PEP8 compliant
- Fields marked read only are no longer processed and populated


0.9.7 (2014-12-22)
^^^^^^^^^^^^^^^^^^

- Added blank_value option for GroupedQuerySelectField
- Add py34 to test matrix
- Fixed midnight handling for TimeField


0.9.6 (2014-09-04)
^^^^^^^^^^^^^^^^^^

- Fixed Unique validator session checking (#19).


0.9.5 (2014-07-31)
^^^^^^^^^^^^^^^^^^

- Fixed base_form option in SplitDateTimeField getting lost if form is initialized more than once.


0.9.4 (2014-07-29)
^^^^^^^^^^^^^^^^^^

- Added base_form option to SplitDateTimeField


0.9.3 (2014-05-15)
^^^^^^^^^^^^^^^^^^

- Fixed InstrumentedAttribute support for Unique validator, issue #13
- Removed CountryField (now part of WTForms-Alchemy)


0.9.2 (2014-03-26)
^^^^^^^^^^^^^^^^^^

- Added WeekDaysField


0.9.1 (2014-01-27)
^^^^^^^^^^^^^^^^^^

- Added new unique validator


0.9.0 (2014-01-14)
^^^^^^^^^^^^^^^^^^

- Deprecated NumberRangeField
- Added IntIntervalField, FloatIntervalField, DecimalIntervalField, DateIntervalField, DateTimeIntervalField
- Updated SQLAlchemy-Utils dependency to version 0.23.0


0.8.3 (2014-01-05)
^^^^^^^^^^^^^^^^^^

- Updated SQLAlchemy-Utils dependency to version 0.22.1


0.8.2 (2013-12-12)
^^^^^^^^^^^^^^^^^^

- Add default validation message for Email validator


0.8.1 (2013-11-30)
^^^^^^^^^^^^^^^^^^

- Fix import error with new versions of `validators` package.
- Added initial WTForms 2.0 support


0.8.0 (2013-10-11)
^^^^^^^^^^^^^^^^^^

- Added Python 3 support


0.7.1 (2013-09-07)
^^^^^^^^^^^^^^^^^^

- Added AjaxField


0.7.0 (2013-08-09)
^^^^^^^^^^^^^^^^^^

- Added GroupedQuerySelectField


0.6.6 (2013-07-31)
^^^^^^^^^^^^^^^^^^

- Added HTML5 compatible basic parameters (disabled, required, autofocus and readonly) for all widgets


0.6.5 (2013-07-30)
^^^^^^^^^^^^^^^^^^

- Added step rendering for NumberInput and RangeInput widgets


0.6.4 (2013-07-22)
^^^^^^^^^^^^^^^^^^

- Packages colour and phonenumbers are now lazy imported


0.6.3 (2013-05-24)
^^^^^^^^^^^^^^^^^^

- Added EmailField to main import
- Added SearchField, IntegerSliderField, DecimalSliderField


0.6.2 (2013-05-24)
^^^^^^^^^^^^^^^^^^

- Added TimeInput, URLInput, ColorInput and TelInput
- Added TimeRange validator


0.6.1 (2013-05-23)
^^^^^^^^^^^^^^^^^^

- Added required flag for NumberInput, DateInput, DateTimeInput
and DateTimeLocalInput whenever associated field has a DataRequired validator.


0.6.0 (2013-05-23)
^^^^^^^^^^^^^^^^^^

- IntegerField and DecimalField which create HTML5 compatible min and max
attributes based on attached NumberRange validators
- DateField, DateTimeField and DateTimeLocalField classes which create HTML5
compatible min and max attributes based on attached NumberRange validators


0.5.5 (2013-05-07)
^^^^^^^^^^^^^^^^^^

- Made TimeField use HTML5 TimeInput
- Made PhoneNumberField use HTML5 TelInput
- Made ColorField use HTML5 ColorInput
- Updated WTForms dependency to 1.0.4


0.5.4 (2013-04-29)
^^^^^^^^^^^^^^^^^^

- Added ColorField


0.5.3 (2013-04-26)
^^^^^^^^^^^^^^^^^^

- Added read_only field marker function


0.5.2 (2013-04-12)
^^^^^^^^^^^^^^^^^^

- Added tests for TimeField
- Added TimeField to main module import


0.5.1 (2013-04-12)
^^^^^^^^^^^^^^^^^^

- Added PassiveHiddenField


0.5.0 (2013-04-04)
^^^^^^^^^^^^^^^^^^

- Added Email validator
- Fixed empty string handling with NumberRange fields


0.4.6 (2013-03-29)
^^^^^^^^^^^^^^^^^^

- Fixed Unique validator when using Form constructor obj parameter
- Updated docs


0.4.5 (2013-03-27)
^^^^^^^^^^^^^^^^^^

- Fixed PhoneNumberField field rendering when validation fails


0.4.4 (2013-03-26)
^^^^^^^^^^^^^^^^^^

- Fixed NumberRangeField field rendering when validation fails


0.4.3 (2013-03-26)
^^^^^^^^^^^^^^^^^^

- Fixed NumberRangeField widget rendering


0.4.2 (2013-03-26)
^^^^^^^^^^^^^^^^^^

- Removed NumberRangeInput


0.4.1 (2013-03-26)
^^^^^^^^^^^^^^^^^^

- Changed empty phone number to be passed as None


0.4.0 (2013-03-26)
^^^^^^^^^^^^^^^^^^

- Added NumberRangeField


0.3.0 (2013-03-26)
^^^^^^^^^^^^^^^^^^

- Changed to use SQLAlchemy-Utils PhoneNumber class


0.2.0 (2013-03-20)
^^^^^^^^^^^^^^^^^^

- Added PhoneNumberField


0.1.0 (2013-03-15)
^^^^^^^^^^^^^^^^^^

- Initial public release
