# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import RequestFactory

from urls.actions import register
from urls.models import UrlRedirect
from datetime import datetime
from urls import constants
from django.http import HttpResponseRedirect
from urls.middleware import UrlRedirectMiddleware

class ActionsTestCase(TestCase):
    def setUp(self):
        date_initial = datetime.strptime('Mon, 10 May 2016 08:30:15 GMT', '%a, %d %B %Y %H:%M:%S GMT')
        date_end = datetime.strptime('Mon, 18 May 2017 08:30:15 GMT', '%a, %d %B %Y %H:%M:%S GMT')
        date_initial3 = datetime.strptime('Mon, 10 May 2016 08:30:15 GMT', '%a, %d %B %Y %H:%M:%S GMT')
        date_end3 = datetime.strptime('Mon, 01 May 2017 08:30:15 GMT', '%a, %d %B %Y %H:%M:%S GMT')

        url_source1='url_source1'
        url_destination1='url_destination1'
        url_source2 = 'url_source2'
        url_destination2 = 'url_destination2'
        url_source3 = 'url_source3'
        url_destination3 = 'url_destination3'
        url1 = UrlRedirect(
            url_source=url_source1,
            url_destination=url_destination1,
            date_initial_validity=date_initial,
            date_end_validity=date_end
        )
        url2 = UrlRedirect(
            url_source=url_source2,
            url_destination=url_destination2,
            date_initial_validity=date_initial,
            date_end_validity=date_end
        )
        url3 = UrlRedirect(
            url_source=url_source3,
            url_destination=url_destination3,
            date_initial_validity=date_initial3,
            date_end_validity=date_end3
        )
        register.update_count_views_url(url_source1)
        url1.save()
        url2.save()
        register.update_count_views_url(url_source1)
        register.update_count_views_url(url_source1)
        url1=UrlRedirect.objects.filter(url_source=url_source1)[0]
        url1.status=constants.STATUS_ARCHIVED
        url1.save()
        register.update_count_views_url(url_source1)
        register.update_count_views_url(url_source3)
        url3.save()
        register.update_count_views_url(url_source3)
        register.update_count_views_url(url_source2)

        self.factory = RequestFactory()
        self.middleware = UrlRedirectMiddleware()
        self.request = self.factory.get('url_source2')

    def test_register_counter_url(self):
        url1 = UrlRedirect.objects.get(url_source="url_source1")
        url2 = UrlRedirect.objects.get(url_source="url_source2")
        url3 = UrlRedirect.objects.get(url_source="url_source3")

        self.assertEquals(url1.url_source, 'url_source1')
        self.assertEquals(url1.views, 2)
        self.assertEquals(url2.url_source, 'url_source2')
        self.assertEquals(url2.views, 1)
        self.assertEquals(url3.views, 0)

    def test_url_redirect_middleware(self):
        response = self.middleware.process_request(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, 'url_destination2')
