# -*- coding: utf-8 -*-
import graphene
from graphene_django import DjangoObjectType
from graphene import relay

from pages.models.page import Page


class PageNode(DjangoObjectType):

    class Meta:
        model = Page
        interfaces = (relay.Node,)