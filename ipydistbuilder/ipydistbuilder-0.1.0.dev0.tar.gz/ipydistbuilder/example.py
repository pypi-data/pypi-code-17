import ipywidgets as widgets
from traitlets import Unicode


@widgets.register('hello.Hello')
class DistBuilder(widgets.DOMWidget):
    """"""
    _view_name = Unicode('DistBuilderView').tag(sync=True)
    _model_name = Unicode('DistBuilderModel').tag(sync=True)
    _view_module = Unicode('ipydistbuilder').tag(sync=True)
    _model_module = Unicode('ipydistbuilder').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    value = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]

