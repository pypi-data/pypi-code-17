from django import template
from django.conf import settings
import markdown2
import bleach


register = template.Library()


@register.filter
def markdownfilter(text):
    untrusted_text = markdown2.markdown(text)
    html = bleach.clean(untrusted_text,
                        tags=settings.MARKDOWNIFY_WHITELIST_TAGS, )
    html = bleach.linkify(html)
    return html
