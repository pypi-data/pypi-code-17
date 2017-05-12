import ttk
from base_widget import BaseWidget


class Combobox(BaseWidget):
    WIDGET = ttk.Combobox
    VAR_TYPE = u'string_var'
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 frame,
                 value=None,
                 trace=None,
                 link=None,
                 bind=None,
                 **kwargs):
        super(Combobox, self).__init__(frame=frame,
                                       value=value,
                                       trace=trace,
                                       link=link,
                                       bind=bind,
                                       **kwargs)

    @property
    def values(self):
        return self.widget[u'values']

    @values.setter
    def values(self,
               values):
        self.config(values=values)