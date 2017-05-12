import ttk
from base_widget import BaseWidget


class Button(BaseWidget):
    WIDGET = ttk.Button
    VAR_TYPE = u'string_var'
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 frame,
                 value=None,
                 trace=None,
                 link=None,
                 bind=None,
                 **kwargs):
        super(Button, self).__init__(frame=frame,
                                     value=value,
                                     trace=trace,
                                     link=link,
                                     bind=bind,
                                     **kwargs)
