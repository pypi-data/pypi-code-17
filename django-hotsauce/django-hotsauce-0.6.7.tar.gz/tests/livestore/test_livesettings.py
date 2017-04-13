from test_support import DjangoTestCase

class ConfigurationGroupTestCase(DjangoTestCase):
    
    def test_import_module(self):
        from livesettings import ConfigurationGroup
