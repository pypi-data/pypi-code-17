# -*- coding: utf-8 -*-
import graphene

from graphene_django import DjangoObjectType

from pages.models.slider import Slider, SliderItem, \
    SliderContentType, SliderContent


class SliderContentNode(DjangoObjectType):

    class Meta:
        model = SliderContent


class SliderContentTypeNode(DjangoObjectType):

    class Meta:
        model = SliderContentType


class SliderItemNode(DjangoObjectType):

    class Meta:
        model = SliderItem


class SliderNode(DjangoObjectType):

    items = graphene.List(SliderItemNode)

    class Meta:
        model = Slider

