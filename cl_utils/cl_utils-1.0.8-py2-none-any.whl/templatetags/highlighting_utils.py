"""
Highlight a string in this node by putting it in a <span class="highlight">

Author: Jonathan Slenders, City Live
"""

from django import template
from django.utils.safestring import mark_safe
from django.template import Library, Node, resolve_variable, VariableDoesNotExist

register = template.Library()
from BeautifulSoup import BeautifulSoup, Tag, NavigableString

import re

# usage: {% highlight_string "classname" "query1" %}... text...{% endhighlight %}
class HighlightNode(Node):
    def __init__(self, nodelist, classname, query):
        self.nodelist = nodelist
        self.classname = classname
        self.query = query

    def render(self, context):
        content = self.nodelist.render(context)
        q = resolve_variable(self.query, context)

        content.replace(q, '<span class="highlight">%s</span>' % q)
        return mark_safe(content)


@register.tag
def highlight_string(parser, token):
    # Nodelist
    nodelist = parser.parse(('endhighlight_string',))
    parser.delete_first_token()

    bits = token.contents.split()[1:]
    assert len(bits) == 2
    classname = bits[0]
    query = bits[1]

    return HighlightNode(nodelist, classname, query)



class HighlightHTMLNode(Node):
    def __init__(self, nodelist, classname, query, inline=False):
        self.nodelist = nodelist
        self.classname = classname
        self.query = query
        self.inline = inline

    def render(self, context):
        tagname = 'span' if self.inline else 'div'
        soup = BeautifulSoup('<%s class="highlighting_container">%s</%s>' %
                (tagname, self.nodelist.render(context), tagname))
        #soup = BeautifulSoup(self.nodelist.render(context))
        classname = resolve_variable(self.classname, context)

        def replace(s):
            """
            Replaces this string in the soup.
            """
            for node in soup.findAll(text=re.compile(re.escape(s), re.IGNORECASE), recursive=True):
                text = unicode(node)

                while text:
                    try:
                        # Find in NavigableString node
                        index = text.lower().index(s.lower())
                    except ValueError:
                        # ValueError: substring not found
                        node_index = node.parent.contents.index(node)
                        node.parent.insert(node_index, NavigableString(text))
                        text = ''
                    else:
                        before = text[:index]
                        after = text[index+len(s):] # recursively

                        # Position of HTML node
                        node_index = node.parent.contents.index(node)

                        node.parent.insert(node_index, NavigableString(before))
                        node_index += 1

                        # Create new highlight tag
                        new_tag = Tag(soup, 'span', [('class', classname), ])
                        new_tag.insert(0, text[index:index+len(s)])
                        node.parent.insert(node_index, new_tag)
                        node_index += 1

                        # Look for another instance in the same node.
                        if s in after:
                            text = after
                        else:
                            node.parent.insert(node_index, NavigableString(after))
                            node_index += 1
                            text = ''

                node.extract()

        # Make soup from HTML
        try:
            for q in self.query:
                q = resolve_variable(q, context)

                if iter(q):
                    for s in q:
                        replace(s)
                                # NOTE: always create new soup after replacing,
                                # because the tree has been changed. (nodes have
                                # been removed.)
                        soup = BeautifulSoup(unicode(soup))
                else:
                    replace(q)
                    soup = BeautifulSoup(unicode(soup))

        except VariableDoesNotExist, e:
            pass

        return unicode(soup)


# usage: {% highlight_html "classname" "query1" "query2" %}... text...{% endhighlight_html %}
# Will place <span> around code.
@register.tag
def highlight_html(parser, token):
    # Nodelist
    nodelist = parser.parse(('endhighlight_html',))
    parser.delete_first_token()

    # items
    bits = token.contents.split()[1:]
    classname = bits[0]
    query = bits[1:]

    return HighlightHTMLNode(nodelist, classname, query)


# usage: {% highlight_inlinehtml "classname" "query1" "query2" %}... text...{% endhighlight_inlinehtml %}
# Will place <div> around code.
@register.tag
def highlight_inlinehtml(parser, token):
    # Nodelist
    nodelist = parser.parse(('endhighlight_inlinehtml',))
    parser.delete_first_token()

    # items
    bits = token.contents.split()[1:]
    classname = bits[0]
    query = bits[1:]

    return HighlightHTMLNode(nodelist, classname, query, inline=True)
