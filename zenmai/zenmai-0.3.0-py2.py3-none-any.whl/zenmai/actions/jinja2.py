import jinja2
import logging
from dictknife import loading
from zenmai.decorators import with_context
logger = logging.getLogger(__name__)


def jinja2_template(template, format=None, load=loading.loads):
    t = jinja2.Template(template, undefined=jinja2.StrictUndefined)

    def render(kwargs):
        s = t.render(**kwargs)
        logger.debug("template: %s", s)
        return load(s, format=format)
    return render


@with_context
def jinja2_templatefile(filename, context, format=None, load=loading.loads):
    template = context.loader.load(filename, format="raw")
    return jinja2_template(template, format=format, load=load)
