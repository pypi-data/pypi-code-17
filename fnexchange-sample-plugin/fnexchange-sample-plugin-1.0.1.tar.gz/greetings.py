from fnexchange.core.plugins import AbstractPlugin


class GreetingsPlugin(AbstractPlugin):
    """
    GreetingsPlugin provides an interface to generate greetings in different languages
    for given users (provided their names and locales).
    At this time, only the following locales are supported: "en-us", "hi-in"

    Request payload schema:
    payload = [
        {"name": "John", "locale": "en-us"},
        ...
        {"name": "Emma", "locale": "hi-in"},
    ]

    Response payload schema:
    payload = [
        {"name": "John", "locale": "en-us", greeting: "Hello, John"},
        ...
        {"name": "Emma", "locale": "en-us", greeting: "Namaste, Emma"},
    ]
    """

    DEFAULT_LOCALE = "en-us"

    hello_map = {
        'en-us': "Hello, {name}! My name is {greeter}",
        'hi-in': "Namaste, {name}! My name is {greeter}",
    }

    bye_map = {
        'en-us': "Goodbye, {name}!",
        'hi-in': "Phir Milenge, {name}!",
    }

    def __greet(self, greeting_map, element):
        name = element["name"]
        locale = element["locale"]
        try:
            greeting = greeting_map[locale].format(name=name, greeter=self.config.greeter)
        except KeyError:
            greeting = "Greetings!"

        return dict(name=name, locale=locale, greeting=greeting)

    def __hello(self, element):
        return self.__greet(self.hello_map, element)

    def __bye(self, element):
        return self.__greet(self.hello_map, element)

    def say_hello(self, payload):
        return {"metadata": {}, "elements": map(self.__hello, payload["elements"])}

    def say_bye(self, payload):
        return {"metadata": {}, "elements": map(self.__bye, payload["elements"])}
