import kivy
kivy.require('1.9.1')

from kivy.properties import ObjectProperty
from codeskeleton.gui.snippetlist import SnippetList

from kivy.app import App


class CodeSkeletonApp(App):
    config = ObjectProperty(None)

    def __init__(self, codeskeleton_config, **kwargs):
        super(CodeSkeletonApp, self).__init__(**kwargs)
        self.codeskeleton_config = codeskeleton_config

    def build(self):
        return SnippetList(codeskeleton_config=self.codeskeleton_config)
