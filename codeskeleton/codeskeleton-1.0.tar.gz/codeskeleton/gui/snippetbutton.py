from kivy.uix.button import Button


class SnippetButton(Button):

    def __init__(self, snippet, **kwargs):
        self.snippet = snippet
        super(SnippetButton, self).__init__(**kwargs)
        self.text = self.snippet.title

    def on_press(self):
        super(SnippetButton, self).on_press()
        print()
        print("*" * 70)
        print()
        print('PRESS')
        print()
        print("*" * 70)
        print()
