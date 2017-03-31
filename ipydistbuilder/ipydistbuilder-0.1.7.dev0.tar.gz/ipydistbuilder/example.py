import ipywidgets as widgets
from traitlets import Unicode, List, Int, TraitError, validate

class DistBuilder(widgets.DOMWidget):
    """"""
    _view_name = Unicode('DistBuilderView').tag(sync=True)
    _model_name = Unicode('DistBuilderModel').tag(sync=True)
    _view_module = Unicode('ipydistbuilder').tag(sync=True)
    _model_module = Unicode('ipydistbuilder').tag(sync=True)
    _view_module_version = Unicode('^0.1.7').tag(sync=True)
    _model_module_version = Unicode('^0.1.7').tag(sync=True)
    width = Int(100).tag(sync=True)
    height = Int(100).tag(sync=True)
    n_bins = Int(10).tag(sync=True)
    n_rows = Int(10).tag(sync=True)
    n_balls = Int(10).tag(sync=True)
    dist = List([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).tag(sync=True)

    @validate('dist')
    def _validate_dist(self, proposal):
        dist = proposal['value']
        if len(dist) != self.n_bins:
            raise TraitError("The distribution does not match the number of bins")
        elif (max(dist) > self.n_rows) or (max(dist) > self.n_rows):
            raise TraitError("The maximum value of the distribution does not match the number of rows")
        else:
            return proposal['value']
