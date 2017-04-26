#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-isnull-list-filter
------------

Tests for `django-isnull-list-filter` models module.
"""
import datetime

from django.core.exceptions import FieldDoesNotExist
from django.test import RequestFactory, TestCase

from isnull_filter import isnull_filter

from model_mommy import mommy

from . import models


class TestIsNullFilter(TestCase):
    def setUp(self):
        albums1 = mommy.make(
            'Album',
            author=None,
            released=datetime.date(2017, 1, 1),
            coauthors=mommy.make(
                'Author',
                _quantity=2,
            ),
            _quantity=2,
        )
        mommy.make(
            'Song',
            album=albums1[1],
        ),
        mommy.make(
            'Album',
            author__name='Mark Knopfler',
            released=None,
            _quantity=8,
        )
        self.factory = RequestFactory()
        self.request = self.factory.get("")

    def test_filter_song_set_yes(self):
        f = isnull_filter('song_set')(self.request, {"song_set__isnull": "true"}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 9)

    def test_filter_song_set_no(self):
        f = isnull_filter('song_set')(self.request, {"song_set__isnull": "false"}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 1)

    def test_filter_song_set_null(self):
        f = isnull_filter('song_set')(self.request, {}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 10)

    def test_filter_author_yes(self):
        f = isnull_filter('author')(self.request, {"author__isnull": "true"}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 2)

    def test_filter_author_no(self):
        f = isnull_filter('author')(self.request, {"author__isnull": "false"}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 8)

    def test_filter_author_null(self):
        f = isnull_filter('author')(self.request, {}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 10)

    def test_filter_coauthors_yes(self):
        f = isnull_filter('coauthors')(self.request, {"coauthors__isnull": "true"}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 8)

    def test_filter_coauthors_no(self):
        f = isnull_filter('coauthors')(self.request, {"coauthors__isnull": "false"}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 2)

    def test_filter_coauthors_null(self):
        f = isnull_filter('coauthors')(self.request, {}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 10)

    def test_filter_released_yes(self):
        f = isnull_filter('released')(self.request, {"released__isnull": "true"}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 8)

    def test_filter_released_no(self):
        f = isnull_filter('released')(self.request, {"released__isnull": "false"}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 2)

    def test_filter_released_null(self):
        f = isnull_filter('released')(self.request, {}, models.Album, None)
        q = f.queryset(self.request, models.Album.objects.all())
        self.assertEquals(q.count(), 10)

    def test_filter_released_title(self):
        f = isnull_filter('released')(self.request, {}, models.Album, None)
        self.assertEquals(f.title, u"Is field 'released' null?")

    def test_filter_song_set_title(self):
        f = isnull_filter('song_set')(self.request, {}, models.Album, None)
        self.assertEquals(f.title, u"Is related 'songs' null?")

    def test_filter_author_title(self):
        f = isnull_filter('author')(self.request, {}, models.Album, None)
        self.assertEquals(f.title, u"Is related 'Authors' null?")

    def test_filter_coauthors_title(self):
        f = isnull_filter('coauthors')(self.request, {}, models.Album, None)
        self.assertEquals(f.title, u"Is related 'Authors' null?")

    def test_filter_title_overriden(self):
        f = isnull_filter('author', 'Overriden title')(self.request, {}, models.Album, None)
        self.assertEquals(f.title, "Overriden title")

    def test_filter_unexistent_field(self):
        with self.assertRaises(FieldDoesNotExist):
            isnull_filter('foo')(self.request, {}, models.Album, None)
