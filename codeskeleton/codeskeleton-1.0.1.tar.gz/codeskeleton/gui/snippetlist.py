from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from codeskeleton import spec
from codeskeleton.gui.snippetbutton import SnippetButton


class SnippetList(ScrollView):

    def __init__(self, codeskeleton_config):
        super(SnippetList, self).__init__()
        self.codeskeleton_config = codeskeleton_config
        snippets = spec.FileSystemLoader(self.codeskeleton_config, spec.Tree).find()
        button_height = 200
        button_container = GridLayout(
            cols=1,
            size_hint_y=None,
            height=button_height * len(snippets)
        )

        for snippet in snippets:
            button_container.add_widget(
                SnippetButton(snippet=snippet,
                              size_hint_y=None,
                              height=button_height))
        self.add_widget(button_container)
