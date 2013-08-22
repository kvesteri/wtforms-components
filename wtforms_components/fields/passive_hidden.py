from wtforms.fields import HiddenField


class PassiveHiddenField(HiddenField):
    """
    HiddenField that does not populate obj values.
    """
    def populate_obj(self, obj, name):
        pass
