"""
GenderField is a field that represents the gender identity of a person. It is
as inclusive as possible, suggesting "simple" genders like "male" and "female"
but also supporting arbitrary text input for non-binary gender identities.
Note that properly using this field requires a bit of Javascript.

Simple example::

    from wtforms import Form
    from wtforms_components import GenderField

    class UserProfileForm(Form):
        gender = GenderField()

To make this field fully functional, you should also add some Javascript to
the page so that when the user selects a non-binary gender, the user is able
to type in their own gender identity. Here is an example script that you can use:

.. code-block:: javascript

    function selectRenderAsText(event) {
        var select = event.target;
        var option = select.selectedOptions[0];
        if("renderAsText" in option.dataset) {
            var input = document.createElement("input");
            input.type = "text";
            input.name = select.name;
            input.id = select.id;
            input.className = select.className;
            input.value = option.value;
            select.parentNode.replaceChild(input, select);
            input.focus()
        };
    }
    function attachRenderAsTextEvents(event) {
        var selects = document.getElementsByTagName("select");
        for (var i = 0; i < selects.length; ++i) {
            selects[i].addEventListener("change", selectRenderAsText);
        }
    }
    document.addEventListener("DOMContentLoaded", attachRenderAsTextEvents);

Or using jQuery:

.. code-block:: javascript

    $(function() {
        $("select").change(function() {
            if("renderAsText" in $("option:selected", this).data()) {
                var input = $("<input>", {
                    "type": "text",
                    "name": $(this).attr("name"),
                    "id": $(this).attr("id"),
                    "class": $(this).attr("class"),
                    "value": $(this).val(),
                });
                $(this).replaceWith(input);
                input.focus();
            }
        });
    });

The field includes the following gender options by default:
"Not Specified", "Male", "Female", and "Non-Binary".
To change these options, pass a list of value-label pairs to the
``simple_genders`` parameter when creating this field. For example, to include
"Transgender" in the dropdown, you could do the following::

    simple_genders = (
        ('', "Not Specified"),
        ('female', "Female"),
        ('male', "Male"),
        ('trans', "Transgender"),
        ('non-binary', "Custom"),
    )

    class UserProfileForm(Form):
        gender = GenderField(simple_genders=simple_genders)

By default, the "Non-Binary" option includes a ``data-render-as-text`` attribute,
which indicates to the Javascript on the page that when the user selects this
option, the ``<select>`` element should transform into an ``<input type="text">``
element so that the user can input an arbitrary gender identity. To change
which option (or options) include this attribute, pass a list of values to
the ``render_as_text`` parameter when creating this field. For example, to
replace the word "Non-binary" with "Genderqueer", you could do the following::

    simple_genders = (
        ('', "Not Specified"),
        ('female', "Female"),
        ('male', "Male"),
        ('genderqueer', "Genderqueer"),
    )

    class UserProfileForm(Form):
        gender = GenderField(
            simple_genders=simple_genders,
            render_as_text=['genderqueer'],
        )

"""

from ..widgets import GenderWidget
from .html5 import StringField


class GenderField(StringField):
    """
    An inclusive gender field. It can render a select field of simple gender
    choices, like "male" and "female", or it can render a string field for
    non-binary gender choices.
    """
    widget = GenderWidget()

    def __init__(
        self,
        label=None,
        validators=None,
        simple_genders=None,
        render_as_text=None,
        **kwargs
    ):
        self.simple_genders = simple_genders or [
            ('', self.gettext('Not Specified')),
            ('male', self.gettext('Male')),
            ('female', self.gettext('Female')),
            ('non-binary', self.gettext('Non-binary')),
        ]
        self.render_as_text = render_as_text or ['non-binary']
        super(GenderField, self).__init__(
            label=label,
            validators=validators,
            **kwargs
        )
