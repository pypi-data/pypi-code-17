import typing
import colored
import datetime
import jinja2
import jinja2.ext
import shlex

from yaz.plugin import Plugin


# todo: use colorama instead of colored.  colorama is likely to already be installed

class Filters:
    @staticmethod
    def quote(value):
        if isinstance(value, jinja2.DebugUndefined):
            return "{{{{ {name}|quote }}}}".format(name=value._undefined_name)
        return shlex.quote(value)

    @staticmethod
    def datetimeformat(value, format):
        assert isinstance(format, str), type(format)
        if isinstance(value, datetime.datetime):
            return value.strftime(format)
        if isinstance(value, str) and value == "now":
            return datetime.datetime.now().strftime(format)
            # todo: return undefined


class ColorExtension(jinja2.ext.Extension):
    tags = set(["color"])

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [jinja2.nodes.Const(None) for _ in range(3)]
        if not parser.stream.current.test("block_end"):
            tuple = parser.parse_tuple()
            if isinstance(tuple, jinja2.nodes.Const):
                args[0] = tuple
            else:
                for index, tuple in zip(range(3), tuple.iter_child_nodes()):
                    args[index] = tuple
        body = parser.parse_statements(["name:endcolor", "name:end_color"], drop_needle=True)
        return jinja2.nodes.CallBlock(self.call_method("_color", args), [], [], body).set_lineno(lineno)

    def _color(self, fg, bg, attr, caller):
        return "".join([colored.fg(fg) if fg else "",
                        colored.bg(bg) if bg else "",
                        colored.attr(attr) if attr else "",
                        caller(),
                        colored.attr("reset") if fg or bg or attr else ""])


class QuoteExtension(jinja2.ext.Extension):
    tags = set(["quote"])

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(["name:endquote", "name:end_quote"], drop_needle=True)
        return jinja2.nodes.CallBlock(self.call_method("_quote"), [], [], body).set_lineno(lineno)

    def _quote(self, caller):
        return Filters.quote(caller())


class Templating(Plugin):
    def __init__(self):
        config = dict(
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=[ColorExtension, QuoteExtension],
            undefined=jinja2.DebugUndefined)
        self.environment = jinja2.Environment(**config)
        self.environment.filters["quote"] = Filters.quote
        self.environment.filters["datetimeformat"] = Filters.datetimeformat

    def render(self, template: str, context: typing.Union[None, dict]):
        assert isinstance(template, str), type(template)
        assert context is None or isinstance(context, dict), type(context)
        return self.environment.from_string(template).render({} if context is None else context)
