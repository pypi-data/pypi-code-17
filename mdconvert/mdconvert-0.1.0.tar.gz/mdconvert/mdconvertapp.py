from IPython.display import display, Javascript
from jupyter_core.application import JupyterApp, base_aliases
from nbconvert.nbconvertapp import NbConvertApp
from nbconvert.exporters.base import get_exporter
from nbconvert.exporters.templateexporter import TemplateExporter
from nbconvert.utils.exceptions import ConversionException
from notebook.services.contents.filemanager import FileContentsManager
from time import time
from traitlets import Bool, CUnicode, Unicode
from traitlets.config.loader import  Config
import json, ruamel_yaml as yaml

# Add additional command line aliases
aliases = dict(base_aliases)

class NbConvertExporter(TemplateExporter):
    filename = Unicode() # no configurable

    def from_filename(self, filename, resources=None, **kw):
        # Capture the filename to convert multiple files.
        self.filename = filename
        return super(NbConvertExporter, self).from_filename(filename, resources, **kw)


    def from_notebook_node(self, nb, resources=None, **kw):
        # track conversion time.
        start_time = time()

        # Preprocess the notebook
        nb, resources = self._preprocess(nb, resources)

        # nbconvert options embedded in the metadata as a dict or a list.
        convert  = nb.metadata.pop('nbconvert', {})
        if isinstance(convert, dict):
            convert = convert.items()

        for exporter, config in convert:
            app = NbConvertApp(config=Config(config))
            app.initialize([])
            app.exporter = get_exporter(exporter)(config=app.config)
            app.convert_single_notebook(self.filename)

        # How long did the conversions take?
        if convert:
            app.log.info(
                "Conversions completed in {} seconds.".format(
                    time()-start_time))

        return


class PostSaveContentsManager(FileContentsManager):
    exporter = NbConvertExporter
    convert = Bool(True)

    def post_save_hook(self, model, os_path, contents_manager):
        if self.convert and model["type"] == "notebook":
            if callable(self.exporter):
                self.exporter = self.exporter(parent=contents_manager)

            contents_manager.parent.io_loop.add_callback(
                 self.exporter.from_filename, os_path
            )

class MDConvertApp(NbConvertApp):
    # Enable some command line shortcuts
    aliases = aliases
    name = 'jupyter-mdconvert'
    export_format = 'mdconvert.mdconvertapp.NbConvertExporter'

    def convert_single_notebook(self, notebook_filename, input_buffer=None):
        try:
            self.exporter.from_filename(notebook_filename)
        except ConversionException:
            self.log.error("Error while converting '%s'", notebook_filename, exc_info=True)
            self.exit(1)

print_metadata = """
this.element.append(
    '<pre><code>'+JSON.stringify(Jupyter.notebook.metadata, null, 4)+'</code></pre>'
);""".strip()

update_metadata = """
var update = %s;
Object.keys(update).forEach(
    function (key){
        var value = update[key];
        if (value){
            Jupyter.notebook.metadata[key] = value
        } else {
            delete Jupyter.notebook.metadata[key];
        };
    });""".strip()

def metadata_magic(line, cell=None):
    """Magic function to update notebook metadata."""
    return display(Javascript(
        cell is None and print_metadata or update_metadata % json.dumps(yaml.load(cell))
    ))

main = launch_instance = MDConvertApp.launch_instance
