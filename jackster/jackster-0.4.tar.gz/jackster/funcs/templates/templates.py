from jinja2 import Environment, ChoiceLoader, PackageLoader, FileSystemLoader,\
    select_autoescape

loaders = [
    FileSystemLoader('templates'),
    PackageLoader('jackster', 'templates')
]
env = Environment(
    loader=ChoiceLoader(loaders),
    autoescape=select_autoescape(['html', 'xml'])
)

def clearLoaders(newLoaders=[]):
    loaders[:] = reversed(newLoaders) + loaders[-1:]
def addLoader(loader):
    loaders.insert(0, loader)

def render(path, content_type='text/html', **kwargs_):
    template = env.get_template(path)
    def func(req, res, nxt, *args, **kwargs):
        res.set_content_type(content_type).set_body(template.render(**{**kwargs_, **kwargs}))
        nxt(*args, **kwargs)
    return func
