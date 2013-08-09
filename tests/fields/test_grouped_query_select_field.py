from wtforms_components import GroupedQuerySelectField
from wtforms_test import FormTestCase
from wtforms import Form


class MultiDict(dict):
    def getlist(self, key):
        return [self[key]]


class Item(object):
    def __init__(self, id, text, group=0):
        self.id = id
        self.text = text
        self.group = group


class TestGroupedQuerySelectField(FormTestCase):
    def setup_method(self, method):
        pass

    def init_form(self, **kwargs):
        class ModelTestForm(Form):
            selector = GroupedQuerySelectField(**kwargs)

        self.form_class = ModelTestForm
        return self.form_class

    def init_form_basic(self):
        return self.init_form(
            query_factory=None,
            get_label=lambda model: u'%s %s' % (
                model.text, model.id
            ),
            get_pk=lambda x: x.id,
            get_group=(
                lambda x: [u'group1', u'group2'][x.group]
                if x.group is not None else None
            ),
            allow_blank=False,
            blank_text=u'No target',
        )

    def test_no_blank_value(self):
        form_class = self.init_form(
            query_factory=None,
            get_label=lambda model: u'%s %s' % (
                model.text, model.id
            ),
            get_pk=lambda x: x.id,
            get_group=(
                lambda x: [u'group1', u'group2'][x.group]
                if x.group is not None else None
            ),
            allow_blank=False,
            blank_text=u'No target',
        )
        items = [Item(12, 'item1'), Item(43, 'item2')]
        form = form_class(MultiDict(selector='12'))
        form.selector.query = items
        html = form.selector()
        assert not u'No target' in html

    def test_show_blank_value(self):
        form_class = self.init_form(
            query_factory=None,
            get_label=lambda model: u'%s %s' % (
                model.text, model.id
            ),
            get_pk=lambda x: x.id,
            get_group=(
                lambda x: [u'group1', u'group2'][x.group]
                if x.group is not None else None
            ),
            allow_blank=True,
            blank_text=u'No target',
        )
        items = [Item(12, 'item1'), Item(43, 'item2')]
        form = form_class(MultiDict(selector='12'))
        form.selector.query = items
        html = form.selector()
        assert u'No target' in html

    def test_defaults_to_blank_value(self):
        form_class = self.init_form(
            query_factory=None,
            get_label=lambda model: u'%s %s' % (
                model.text, model.id
            ),
            get_pk=lambda x: x.id,
            get_group=(
                lambda x: [u'group1', u'group2'][x.group]
                if x.group is not None else None
            ),
            allow_blank=True,
            blank_text=u'No target',
        )
        items = [Item(12, 'item1'), Item(43, 'item2')]
        form = form_class()
        form.selector.query = items
        html = form.selector()
        assert u'<option selected="selected" value="__None">No target' in html

    def test_submit_valid_item(self):
        form_class = self.init_form_basic()
        items = [Item(12, 'item1'), Item(43, 'item2')]
        form = form_class(MultiDict(selector='12'))
        form.selector.query = items
        form.validate()
        assert len(form.errors) == 0

    def test_submit_invalid_item(self):
        form_class = self.init_form_basic()
        items = [Item(12, 'item1'), Item(43, 'item2')]
        form = form_class(MultiDict(selector='14'))
        form.selector.query = items
        form.validate()
        assert len(form.errors) == 1

    def test_dont_show_empty_group(self):
        form_class = self.init_form_basic()
        items = [Item(12, 'item1'), Item(43, 'item2')]
        form = form_class(MultiDict(selector='12'))
        form.selector.query = items
        html = form.selector()
        assert not u'group2' in html

    def test_grouped_items(self):
        form_class = self.init_form_basic()
        items = [Item(12, 'item1', 0), Item(43, 'item2', 1)]
        form = form_class(MultiDict(selector='14'))
        form.selector.query = items
        html = form.selector()
        assert u'group1' in html
        assert u'group2' in html

    def test_grouped_and_non_grouped_items(self):
        form_class = self.init_form_basic()
        items = [
            Item(8, 'item1', None),
            Item(12, 'item2', 0),
            Item(43, 'item3', 0)
        ]
        form = form_class(MultiDict(selector='14'))
        form.selector.query = items
        html = form.selector()

        import re
        expression = re.compile(r".*item1 8.*group1.*item2 12.*item3 43")
        assert expression.match(html.replace('\n', ''))
