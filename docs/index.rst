WTForms-Components
==================

WTForms-Components provides various additional fields, validators and widgets
for WTForms.

Fields
======


SelectField
-----------

WTForms-Components provides enhanced versions of WTForms SelectFields. Both WTForms-Components
SelectField and SelectFieldMultiple support optgroups.

PhoneNumberField
----------------

PhoneNumberField is a string field representing a PhoneNumber object from
`SQLAlchemy-Utils`_.

.. _SQLAlchemy-Utils:
   https://github.com/kvesteri/sqlalchemy-utils

The following example shows that the field takes the phone number's country
code and display format as parameters. ::

    from wtforms import Form
    from wtforms_components import PhoneNumberField

    class UserForm(Form):
        phone_number = PhoneNumberField(
            country_code='FI'
            display_format='national'
        )

Validators
==========

DateRange validator
-------------------

The DateRange validator is essentially the same as wtforms.validators.NumberRange validator but validates
dates.

In the following example we define a start_time field, which does not accept dates in the past. ::

    from datetime import datetime
    from wtforms import Form
    from wtforms.fields import DateField
    from wtforms_components import DateRange

    class EventForm(Form):
        start_time = DateField(
            validators=[DateRange(min=datetime.now())]
        )

If validator
------------

The If validator provides means for having conditional validations. In the following example we only
validate field email if field user_id is provided. ::


    from wtforms import Form
    from wtforms.fields import IntegerField, TextField
    from wtforms_components import If

    class SomeForm(Form):
        user_id = IntegerField()
        email = TextField(validators=[
            If(lambda form, field: form.user_id.data, Email())
        ])


Chain validator
---------------


Chain validator chains validators together. Chain validator can be combined with If validator
to provide nested conditional validations. ::


    from wtforms import Form
    from wtforms.fields import IntegerField, TextField
    from wtforms_components import If

    class SomeForm(Form):
        user_id = IntegerField()
        email = TextField(validators=[
            If(
                lambda form, field: form.user_id.data,
                Chain(DataRequired(), Email())
            )
        ])


Unique Validator
----------------

Unique validator provides convenient way for checking the unicity of given field in database.

Let's say we have the following model defined (using SQLAlchemy):
::


    import sqlalchemy as sa
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///:memory:')
    Base = declarative_base(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    class User(Base):
        __tablename__ = 'user'

        id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
        name = sa.Column(sa.Unicode(100), nullable=False)
        email = sa.Column(sa.Unicode(255), nullable=False)


Now creating a form that validates email unicity is as easy as:
::


    from wtforms_components import ModelForm, Unique

    class UserForm(ModelForm):
        name = TextField()
        email = TextField(validators=[
            Unique(
                User.email,
                get_session=lambda: session
            )
        ])

