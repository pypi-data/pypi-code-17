from jinja2 import Environment, FileSystemLoader, select_autoescape

defaultEnv = None
def setPath(path):
    global defaultEnv
    defaultEnv = Environment(
        loader=FileSystemLoader(path),
        autoescape=select_autoescape(['html', 'xml'])
    )
setPath('templates')

def render(path, env=defaultEnv, content_type='text/html'):
    template = env.get_template(path)
    def func(req, res, nxt, *args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                kwargs = {**arg, **kwargs}
        res.contentType(content_type).body(template.render(**kwargs))
        nxt()
    return func
