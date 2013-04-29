from cgi import escape
from wtforms.widgets import (
    HTMLString, html_params, TextInput, Select as BaseSelectWidget
)


class PhoneNumberInput(TextInput):
    input_type = 'tel'


class ReadOnlyWidgetProxy(object):
    def __init__(self, widget):
        self.widget = widget

    def __getattr__(self, name):
        return getattr(self.widget, name)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('readonly', True)
        return self.widget(field, **kwargs)


class SelectWidget(BaseSelectWidget):
    """
    Add support of choices with ``optgroup`` to the ``Select`` widget.
    """
    @classmethod
    def render_option(cls, value, label, mixed):
        """
        Render option as HTML tag, but not forget to wrap options into
        ``optgroup`` tag if ``label`` var is ``list`` or ``tuple``.
        """
        if isinstance(label, (list, tuple)):
            children = []

            for item_value, item_label in label:
                item_html = cls.render_option(item_value, item_label, mixed)
                children.append(item_html)

            html = u'<optgroup label="%s">%s</optgroup>'
            data = (escape(unicode(value)), u'\n'.join(children))
        else:
            coerce_func, data = mixed
            if isinstance(data, list) or isinstance(data, tuple):
                selected = coerce_func(value) in data
            else:
                selected = coerce_func(value) == data

            options = {'value': value}

            if selected:
                options['selected'] = u'selected'

            html = u'<option %s>%s</option>'
            data = (html_params(**options), escape(unicode(label)))

        return HTMLString(html % data)
