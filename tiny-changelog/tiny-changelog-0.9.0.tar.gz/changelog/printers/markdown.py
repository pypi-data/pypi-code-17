from .printer import Printer


class MarkdownPrinter(Printer):
    def header(self):
        return u'# Change Log\n'

    def footer(self):
        return u''

    def break_line(self):
        return u'\n'

    def tag_line(self, tag):
        return u'# [{name}]({url})\n'.format(**tag.as_dict)

    def pr_line(self, pr):
        return u'* [\#{number}]({url}) {title} (@{author})\n'.format(
            **pr.as_dict)

    def iteritems(self):
        yield self.header()
        yield self.break_line()

        for tag, pull_requests in super(MarkdownPrinter, self).iteritems():
            yield self.tag_line(tag)
            for pr in pull_requests:
                yield self.pr_line(pr)
            yield self.break_line()

        yield self.footer()
