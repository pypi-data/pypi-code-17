import jinja2
from dictknife import loading


def jinja2_template(template, format="yaml", load=loading.loads):
    t = jinja2.Template(template, undefined=jinja2.StrictUndefined)

    def render(kwargs):
        s = t.render(**kwargs)
        return load(s, format=format)
    return render
