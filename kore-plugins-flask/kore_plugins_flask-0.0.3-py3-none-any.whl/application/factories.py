class ApplicationFactory(object):

    def __init__(self, config_factory, container_factory):
        self.config_factory = config_factory
        self.container_factory = container_factory

    def create(self, config_type, **config_opt):
        config = self.config_factory.create(config_type, **config_opt)
        container = self.container_factory.create(config=config)
        return container('kore.components.flask.application')
