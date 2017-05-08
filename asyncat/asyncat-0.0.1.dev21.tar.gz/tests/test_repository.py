#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""asyncat.repo test cases."""
from __future__ import print_function, division, unicode_literals

from tornado import testing

from asyncat import repository
from asyncat.client import GithubError

from . import AsyncatTestCase


class RepositoryTestCase(AsyncatTestCase):
    """Repository test case."""
    def setUp(self):
        """Setup"""
        super(RepositoryTestCase, self).setUp()
        self.repo = repository.Repository(self.client, "asyncat", "demo")

    @testing.gen_test
    def test_sync(self):
        """Synchronizes repository."""
        yield self.repo.sync()
        self.assertEqual(self.repo.c["id"], 90337889)

    @testing.gen_test
    def test_pull_not_exists(self):
        """Pull request not exists."""
        try:
            yield self.repo.pull(404)
        except GithubError as e:
            self.assertEqual(e.status_code, 404)

    @testing.gen_test
    def test_pull(self):
        """Pull Request is ok."""
        pull = yield self.repo.pull(1)
        self.assertEqual(pull.c["title"], "Create demo.txt")

    @testing.gen_test
    def test_comment(self):
        """Comment on Pull Request."""
        pull = yield self.repo.pull(1)
        self.assertEqual(pull.c["title"], "Create demo.txt")
        yield pull.create_comment("Test Comment")

    @testing.gen_test
    def test_merge_and_ref(self):
        """Create ref & merge ref & update ref"""
        base_sha = "b1b0845dfd9397059c4d0557a8431f4cae786a17"
        ref = self.repo.ref("heads/auto")
        try:
            resp = yield ref.create(base_sha)
            yield ref.sync()
            self.assertEqual(ref.c["ref"], "refs/heads/auto")
            self.assertEqual(ref.c["object"]["sha"], base_sha)

            resp = yield self.repo.merge("auto", "merge-test",
                                         "Merge merge-test to auto")
            self.assertEqual(resp.code, 201)
            resp = yield ref.update(base_sha, force=True)
            self.assertEqual(resp.data["object"]["sha"], base_sha)
        finally:
            resp = yield ref.delete()
            self.assertEqual(resp.code, 204)

    @testing.gen_test
    def test_status(self):
        """Create status."""
        sha = "805356407393aacf4d810d07aad260c01cc8e8ad"
        resp = yield self.repo.create_status(sha, "pending")
        self.assertEqual(resp.code, 201)

    @testing.gen_test
    def test_list_statuses(self):
        """List statues."""
        sha = "805356407393aacf4d810d07aad260c01cc8e8ad"
        resp = yield self.repo.get_statuses(sha)
        self.assertEqual(resp.code, 200)

    @testing.gen_test
    def test_pull_create_and_update(self):
        """Create and update pull request."""
        pull = yield self.repo.create_pull("Test Pull", "feature-pull",
                                           "master", "test body")
        pull.state = "closed"
        pull.title = "[Closed] " + pull.title
        yield pull.update()
