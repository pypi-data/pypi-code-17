import morepath
from pymitter import EventEmitter


class App(morepath.App):
    signal = EventEmitter()
