__author__ = 'Artur Maciąg'
__email__ = 'maciag.artur@gmail.com'
__version__ = '0.0.4'
__url__ = 'https://github.com/kore-plugins/kore-plugins-flask'

from kore import config_factory, container_factory

from kore_plugins_flask.application.factories import ApplicationFactory

application_factory = ApplicationFactory(config_factory, container_factory)
