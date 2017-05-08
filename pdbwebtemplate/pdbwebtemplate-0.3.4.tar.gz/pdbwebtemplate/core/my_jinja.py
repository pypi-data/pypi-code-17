import jinja2

class Jinja():

    __jinja_env = None

    @classmethod
    def get_jinja_object(cls):
        if not cls.__jinja_env:
            cls.__jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('app'),
                                                 autoescape=True, extensions=['jinja2.ext.autoescape'])

        return cls.__jinja_env