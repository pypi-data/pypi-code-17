# -*- coding: utf-8 -*-
from graphene_django import DjangoObjectType

from pages.models.page import Page


class PageNode(DjangoObjectType):

    class Meta:
        model = Page
