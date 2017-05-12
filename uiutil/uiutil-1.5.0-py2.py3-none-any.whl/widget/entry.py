import ttk
from base_widget import BaseWidget


class TextEntry(BaseWidget):
    WIDGET = ttk.Entry
    VAR_TYPE = u'string_var'
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 frame,
                 value=None,
                 trace=None,
                 link=None,
                 bind=None,
                 **kwargs):
        super(TextEntry, self).__init__(frame=frame,
                                        value=value,
                                        trace=trace,
                                        link=link,
                                        bind=bind,
                                        **kwargs)
class IntEntry(BaseWidget):
    WIDGET = ttk.Entry
    VAR_TYPE = u'int_var'
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 frame,
                 value=None,
                 trace=None,
                 link=None,
                 bind=None,
                 **kwargs):
        super(IntEntry, self).__init__(frame=frame,
                                       value=value,
                                       trace=trace,
                                       link=link,
                                       bind=bind,
                                       **kwargs)
