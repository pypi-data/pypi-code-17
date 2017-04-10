# -*- coding: utf-8 -*-
# pylint: disable=import-error
'''
Template filters for extracting dominant colour or colour palette from
an image.
'''

import colorgram

from django import template


register = template.Library()


def clamp(number):
    '''
    Ensure a colour channel value is within proper bounds.
    '''
    return max(0, min(number, 255))


@register.filter
def imagecolor(image):
    '''
    Return the dominant colour from the image object.
    '''
    colors = colorgram.extract(image, 6)
    first_color = colors[0]
    rgb = first_color.rgb
    hexcolor = "#{0:02x}{1:02x}{2:02x}".format(clamp(rgb.r), clamp(rgb.g), clamp(rgb.b))

    return hexcolor
