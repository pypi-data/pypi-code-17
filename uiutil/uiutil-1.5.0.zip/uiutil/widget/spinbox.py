from ttk_spinbox import Spinbox as ttk_spinbox
from base_widget import BaseWidget


class Spinbox(BaseWidget):
    WIDGET = ttk_spinbox
    VAR_TYPE = u'int_var'
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 frame,
                 value=None,
                 trace=None,
                 link=None,
                 bind=None,
                 **kwargs):
        super(Spinbox, self).__init__(frame=frame,
                                      value=value,
                                      trace=trace,
                                      link=link,
                                      bind=bind,
                                      **kwargs)