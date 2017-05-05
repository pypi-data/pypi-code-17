# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from pages.schema import schema
from pages.models.page import Page


class PageTestCase(TestCase):

    def setUp(self):
        self._create_pages()

    def _create_pages(self):
        page = Page()
        page.title = 'Test Page'
        page.external_url = 'https://www.crehana.com/'
        page.is_active = True
        page.save()

    def get_page_query(self):
        query = '''
                    {
                       pages {
                         title
                         slug
                         external_url
                         is_active
                       }
                     }
                '''
        return query

    def test_get_pages(self):
        result = schema.execute(self.get_page_query())
        pages = result.data.get('pages', [])
        self.assertEquals(len(pages), 1)

    def test_register_page(self):
        result = schema.execute(self.get_page_query())
        pages = result.data.get('pages', [])
        self.assertEquals(len(pages), 1)

    # def test_upload_page(self):
    #     result = schema.execute(self.get_page_query())
    #     pages = result.data.get('pages', [])
    #     self.assertEquals(len(pages), 1)
    #
    # def test_security(self):
    #     result = schema.execute(self.get_page_query())
    #     pages = result.data.get('pages', [])
    #     self.assertEquals(len(pages), 1)