from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Fix for the 'wontfix' at https://code.djangoproject.com/ticket/3371

    Maybe someday the django developers will realize that getting things
    out of dictionaries is a common workflow, until either that happens
    or the Constellation suite abandons Django's templating engine
    entirely for the much more sane Jinja2, we will use this function as
    described here:
    http://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
"""
    return dictionary.get(key)

