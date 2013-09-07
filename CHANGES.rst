Changelog
---------

Here you can see the full list of changes between each WTForms-Components
release.


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
