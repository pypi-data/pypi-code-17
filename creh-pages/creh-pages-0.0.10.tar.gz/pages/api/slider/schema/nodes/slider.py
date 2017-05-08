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

    picture_url = graphene.String()

    contents = graphene.List(SliderContentNode)

    class Meta:
        model = SliderItem

    def resolve_picture_url(self, args, request, info):
        return self.picture_url

    def resolve_contents(self, args, request, info):
        return self.slidercontent_set.all()


class SliderNode(DjangoObjectType):

    items = graphene.List(SliderItemNode)

    class Meta:
        model = Slider

    def resolve_items(self, args, request, info):
        return self.slideritem_set.all()

