from django import template
from django.utils.safestring import mark_safe
from BeautifulSoup import BeautifulSoup, Comment
import re

register = template.Library()

@register.filter
def user_input(value):

    html = value

    #Beautiful Soup
    valid_tags = 'p i strong em ol ul li b u a blockquote pre br img embed div span object param table tr td th'.split()
    valid_attrs = 'href src alt align border title style rel name value width height data type hspace vspace'.split()

            # hspace/vspace attrs are required for CKEdit, margin around images.

    soup = BeautifulSoup(html)

    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = [(attr, val) for attr, val in tag.attrs
                     if attr in valid_attrs]

    souped = soup.renderContents().decode('utf-8')

    #Strip javascript
    #gnarly regex to look for `javascript:` in the text
    regex = re.compile(
            'j[\s]*(&#x.{1,7})?a[\s]*(&#x.{1,7})?v[\s]*(&#x.{1,7})?a[\s]*(&#x.{1,7})?s[\s]*(&#x.{1,7})?c[\s]*(&#x.{1,7})?r[\s]*(&#x.{1,7})?i[\s]*(&#x.{1,7})?p[\s]*(&#x.{1,7})?t',
        re.IGNORECASE)
    cleaned = regex.sub('', souped)


    # Postprocessing: remove comments
    # We noticed that beautifulsoup had difficulties parsing "<! <!-- ",
    # which was literally send to the output

	# Remove comments like <!-- ... -->
    cleaned = re.sub(ur'<!--([^-]|-(?!-)|--(?!>))*-->', u'', cleaned)
	# Remove any remaining <!, just to be sure...
    cleaned = re.sub(ur'<!', u'', cleaned)

    return mark_safe(cleaned)
user_input.is_safe = True
