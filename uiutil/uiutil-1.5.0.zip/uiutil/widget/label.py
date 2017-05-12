import ttk
from base_widget import BaseWidget


class Label(BaseWidget):
    WIDGET = ttk.Label
    VAR_TYPE = u'int_var'
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 frame,
                 value=None,
                 trace=None,
                 link=None,
                 bind=None,
                 **kwargs):
        super(Label, self).__init__(frame=frame,
                                    value=value,
                                    trace=trace,
                                    link=link,
                                    bind=bind,
                                    **kwargs)