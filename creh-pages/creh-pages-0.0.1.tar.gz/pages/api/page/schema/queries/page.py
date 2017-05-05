# -*- coding: utf-8 -*-
import graphene

from graphene import AbstractType

from pages.models.page import Page
from pages.api.page.schema.nodes.page import PageNode


class PageQuery(AbstractType):
    page = graphene.Field(PageNode, id=graphene.String(), slug=graphene.String())
    pages = graphene.List(PageNode, description='listado de paginas')

    def resolve_pages(self, args, context, inf):
        return Page.objects.filter(
            is_active=True,
        )

    def resolve_page(self, args, context, inf):
        course = Page.objects.none()
        if args.get('id', None):
            return Page.objects.get(id=args.get('id', None), is_active=True)
        elif args.get('slug', None):
            course = Page.objects.get(slug=args.get('slug', None), is_active=True)
        return course
