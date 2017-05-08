# -*- coding: utf-8 -*-
import graphene

from graphene_django import DjangoObjectType

from pages.models.slider import Slider, SliderItem, \
    SliderContentType, SliderContent


class SliderNode(DjangoObjectType):

    items = graphene.List(SliderItemNode)

    class Meta:
        model = Slider


class SliderItemNode(DjangoObjectType):

    class Meta:
        model = SliderItem


class SliderContentTypeNode(DjangoObjectType):

    class Meta:
        model = SliderContentType


class SliderContentNode(DjangoObjectType):

    class Meta:
        model = SliderContent

