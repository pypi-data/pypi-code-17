# -*- coding: utf-8 -*-
import graphene
from graphene_django import DjangoObjectType
from graphene import relay

from pages.models.slider import Slider


class SliderNode(DjangoObjectType):

    class Meta:
        model = Slider
        interfaces = (relay.Node,)