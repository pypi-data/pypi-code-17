
from Tkinter import NORMAL, DISABLED

from ..mixin import WidgetMixIn, VarMixIn


class BaseWidget(WidgetMixIn,
                 VarMixIn):

    # Define WIDGET when subclassing.
    # It should be a ttk widget, e.g ttk.Button
    #
    # Define VAR_TYPE when subclassing.
    # It should be a VarMixIn type, e.g self.string_var
    #
    # Define VAR_PARAM when subclassing.
    # It should be the parameter name into WIDGET that takes the variable, e.g. textvariable

    def __init__(self,
                 frame,
                 value=None,
                 trace=None,
                 link=None,
                 bind=None,
                 **kwargs):

        # TODO: Add hooks for further customisation (e.g so that Switch can be based on this)
        if not self.WIDGET:
            raise NotImplementedError(u'WIDGET must be defined')

        if not self.VAR_TYPE:
            raise NotImplementedError(u'VAR_TYPE must be defined')

        if not self.VAR_PARAM:
            raise NotImplementedError(u'VAR_PARAM must be defined')

        super(BaseWidget, self).__init__(parent=frame, **kwargs)

        self.frame = frame

        # Declare the var
        var_type = getattr(self, self.VAR_TYPE)
        self.var = var_type(trace=trace,
                            link=link,
                            value=value)

        kwargs[self.VAR_PARAM] = self.var

        if kwargs.get(u'tooltip'):
            self.widget, self.tooltip = self.add_widget_and_position(
                                            widget=self.WIDGET,
                                            frame=self.frame,
                                            **kwargs)
        else:
            self.widget = self.frame.add_widget_and_position(
                              widget=self.WIDGET,
                              **kwargs)
        if bind:
            self.bind(*bind)

    @property
    def value(self):
        return self.var.get()

    @value.setter
    def value(self,
              value):
        self.var.set(value)

    def enable(self):
        self.widget.config(state=NORMAL)

    def disable(self):
        self.switch.config(state=DISABLED)

    def config(self,
               **params):
        self.widget.config(**params)

    def bind(self,
             *args,
             **kwargs):
        self.widget.bind(*args,
                         **kwargs)
