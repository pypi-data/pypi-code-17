from __future__ import print_function
import time
import os
import ipywidgets as widgets
import base64
from string import Template
from IPython.display import HTML, Javascript, display


js_template = """
<script type="text/Javascript">
  function handle${name}(evt) {
    var results, command;
    var kernel = IPython.notebook.kernel;
    var file = evt.target.files[0];
    kernel.execute('from hublib.ui import FileUpload')
    var that = this;
    if (file) {
        var fileReader = new FileReader();
        fileReader.onload = function fileReaderOnload () {
            results = fileReader.result;
            cmd = 'FileUpload.obj["${name}"].data="' + results + '"';
            kernel.execute(cmd)
        };
        fileReader.readAsDataURL(file);
    } else {
        console.log('Unable to open file.', file);
    }

    cmd = 'FileUpload.obj["${name}"].type="' + file.type + '";';
    cmd += 'FileUpload.obj["${name}"].name="' + file.name + '"';
    kernel.execute(cmd);
  }
  document.getElementById('fs_${name}').addEventListener('change', handle${name}, false);
</script>
"""


class FileUpload(object):
    obj = {}

    def __init__(self, name, desc, **kwargs):
        width = kwargs.get('width', 'auto')
        form_item_layout = widgets.Layout(
            display='flex',
            flex_flow='row',
            border='solid 1px lightgray',
            justify_content='space-between',
            width=width
        )
        self.vname = FileUpload.make_vname()
        FileUpload.obj[self.vname] = self
        self._data = None
        self._name = ""
        self._type = ""

        input_form = '<input type="file" id="fs_%s" name="files[]"/>' % self.vname
        d = dict(name=self.vname)
        js = Template(js_template).substitute(d)
        self.input = widgets.HTML(value=input_form + js,
                                  layout=widgets.Layout(flex='2 1 auto'))
        self.label = widgets.HTML(value='<p data-toggle="popover" title="%s">%s</p>' % (desc, name),
                                  layout=widgets.Layout(flex='2 1 auto'))
        self.w = widgets.Box([self.label, self.input], layout=form_item_layout)

    def save(self, name=None):
        if self.name == "":
            raise IOError("No file or data found.")

        if name is None:
            name = self.name

        with open(name, 'w') as f:
            f.write(self.data)


    @property
    def name(self):
       return self._name

    @name.setter
    def name(self, val):
        self._name = val


    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        if val is None:
            self._data = None
            return
        self._data = base64.b64decode(val.split(',', 1)[1])

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        self._type = val

    @property
    def visible(self):
        return self.w.layout.visibility

    @visible.setter
    def visible(self, newval):
        if newval:
            self.w.layout.visibility = 'visible'
            return
        self.w.layout.visibility = 'hidden'

    def _ipython_display_(self):
        self.w._ipython_display_()

    @staticmethod
    def make_vname():
        t = str(time.time()).replace('.', '_')
        return "v_%s" % t
