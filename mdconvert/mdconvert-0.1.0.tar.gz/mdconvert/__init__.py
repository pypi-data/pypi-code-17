from .mdconvertapp import launch_instance, metadata_magic, PostSaveContentsManager  # noqa
from ._version import __version__  # noqa

from IPython import get_ipython

def load_ipython_extension(ip):
    get_ipython().register_magic_function(
        metadata_magic, magic_kind='line_cell', magic_name='metadata'
    )

def _jupyter_server_extension_paths():
    return [{
        "module": "mdconvert"
    }]

def load_jupyter_server_extension(nb_app):
    nb_app.web_app.settings.update(
        contents_manager=PostSaveContentsManager(parent=nb_app, log=nb_app.log)
    )
