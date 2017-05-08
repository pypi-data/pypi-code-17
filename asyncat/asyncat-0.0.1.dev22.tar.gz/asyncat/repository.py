#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" Implement Github operation """
from __future__ import print_function, division, unicode_literals

from tornado import gen

from .enumeration import StatusState


class GithubEntity(object):
    """A object represents the entity of Github."""
    def __init__(self, client, *args, **kwargs):
        """Initialize

        :param client: Github client instance
        :type client: :class:`~asyncat.client.AsyncGithubClient`
        :param *args: arguments to initialize
        :param **kargs: keyword arguments to initialize
        """
        #: Entity content
        self.c = {}
        self.client = client
        self.initialize(*args, **kwargs)
        self._sync_info = {}

    def initialize(self):
        """Override this method to initialize in subclass."""
        pass        # pragma: no cover

    @gen.coroutine
    def sync(self):
        """Synchronize with Github, use Github's data to fill current entity.

        :returns: self
        """
        resp = yield self.do_sync()
        self.c = resp.data
        self.after_sync()
        raise gen.Return(self)

    def after_sync(self):
        """This function will call after ``do_sync``."""
        pass

    def do_sync(self):
        """Override this method to implemente synchronizes with Github.
        This method must returns an instance of
        :class:`tornado.concurrent.Future`
        """
        raise NotImplementedError()     # pragma: no cover

    def make(self, entity_cls, *args, **kwargs):
        """Make an entity."""
        return entity_cls(self.client, *args, **kwargs)


class _CommentMixin(object):        # pylint: disable=R0903
    """Comment mixin to add `create_comment` method to an entity."""
    def create_comment(self, body):
        """Create comment on issues or pull requests.

        See also:
            https://developer.github.com/v3/issues/comments/#create-a-comment
        """
        return self.client.request(
            "{}/issues/{}/comments".format(self.repo.base_path, self.num),
            params={"body": body},
            method="POST"
        )


class PullRequest(GithubEntity, _CommentMixin):     # pylint: disable=R0902
    """Representes a pull reuqest of Github.

    See also: https://developer.github.com/v3/pulls/#get-a-single-pull-request
    """
    def initialize(self, repo, num):
        """Initialize

        :type repo: :class:`Repository`
        :param num: number of pull request
        """
        self.repo = repo
        self.num = num

        self.title = None
        self.body = None
        self.state = None
        self.base = None
        self.maintainer_can_modify = None

    def after_sync(self):
        """Set property after synchronize."""
        self.title = self.c["title"]
        self.body = self.c["body"]
        self.state = self.c["state"]
        self.base = self.c["base"]["ref"]
        self.head = self.c["head"]["ref"]
        self.maintainer_can_modify = self.c["maintainer_can_modify"]

    @gen.coroutine
    def create(self):
        """Create a pull request."""
        resp = yield self.client.request(
            self.repo.base_path + "/pulls", params={
                "title": self.title,
                "head": self.head,
                "base": self.base,
                "body": self.body,
                "maintainer_can_modify": self.maintainer_can_modify
            },
            method="POST")
        self.c = resp.data
        self.after_sync()
        self.num = self.c["number"]
        raise gen.Return(self)

    @gen.coroutine
    def update(self):
        """Update current pull request. Before call this function you must
        set current instance's property to update.
        """
        resp = yield self.client.request(
            "{}/pulls/{}".format(self.repo.base_path, self.num),
            params={
                "title": self.title,
                "body": self.body,
                "state": self.state,
                "base": self.base,
                "maintainer_can_modify": self.maintainer_can_modify,
            }, method="PATCH")
        self.c = resp.data
        self.after_sync()
        raise gen.Return(self)

    def do_sync(self):
        """Synchronize."""
        return self.client.request(
            '{}/pulls/{}'.format(self.repo.base_path, self.num))


class Issue(GithubEntity, _CommentMixin):       # pylint: disable=R0902
    """Representes an issue of Github."""
    def initialize(self, repo, num):
        """Initialize

        :type repo: :class:`Repository`
        :param num: Issue number.
        """
        self.repo = repo
        self.num = num
        self.title = None
        self.body = None
        self.state = "open"
        self.milestone = None
        self.labels = []
        self.assignees = []

    def after_sync(self):
        """Set property after synchronize."""
        self.num = self.c["number"]
        self.title = self.c["title"]
        self.body = self.c["body"]
        self.state = self.c["state"]

        if self.c["milestone"]:
            self.milestone = self.c["milestone"]["number"]
        else:
            self.milestone = None

        self.assignees = [x["login"] for x in self.c["assignees"]]
        self.labels = self.c["labels"]

    @gen.coroutine
    def create(self):
        """Create an issue."""

        params = {
            "title": self.title,
            "body": self.body,
            "labels": self.labels or [],
            "assignees": self.assignees or [],
        }

        if self.milestone:
            params["milestone"] = self.milestone

        resp = yield self.client.request(
            self.repo.base_path + "/issues",
            params=params, method="POST")
        self.c = resp.data
        self.after_sync()
        raise gen.Return(self)

    @gen.coroutine
    def update(self):
        """Use property update current issue."""

        params = {
            "title": self.title,
            "body": self.body,
            "state": self.state,
            "labels": self.labels,
            "assignees": self.assignees,
        }

        if self.milestone:
            params["milestone"] = self.milestone

        resp = yield self.client.request(
            "{}/issues/{}".format(self.repo.base_path, self.num),
            params=params, method="PATCH")
        self.c = resp.data
        self.after_sync()
        raise gen.Return(self)

    def do_sync(self):
        """Synchronize."""
        return self.client.request("{}/issues/{}".format(self.repo.base_path,
                                                         self.num))


class Reference(GithubEntity):
    """Reference."""
    def initialize(self, repo, ref):
        """Initialize

        :type repo: :class:`Repository`
        :param ref:
            Reference in url.
            See also:
                https://developer.github.com/v3/git/refs/#update-a-reference
        """
        self.repo = repo
        self.ref = ref[5:] if ref.startswith("refs/") else ref

    def do_sync(self):
        """Synchronizing."""
        return self.client.request(
            "{}/git/refs/{}".format(self.repo.base_path, self.ref))

    def create(self, sha):
        """Create a reference

        See also: https://developer.github.com/v3/git/refs/#create-a-reference
        """
        return self.client.request(
            self.repo.base_path + "/git/refs",
            params={
                "ref": "refs/" + self.ref,
                "sha": sha
            }, method="POST")

    def update(self, sha, force=False):
        """Update a reference

        See also: https://developer.github.com/v3/git/refs/#update-a-reference
        """
        return self.client.request(
            self.repo.base_path + "/git/refs/" + self.ref,
            params={
                "sha": sha,
                "force": force,
            }, method="PATCH")

    def delete(self):
        """Delete current reference."""
        return self.client.request(
            self.repo.base_path + "/git/refs/" + self.ref, method="DELETE")


class Repository(GithubEntity):
    """Representes a repository of Github."""
    def initialize(self, owner, label):
        self.owner = owner
        self.label = label

    def do_sync(self):
        """Synchronizing."""
        return self.client.request(self.base_path)

    @property
    def base_path(self):
        """Path of this repository."""
        return "/repos/{}/{}".format(self.owner, self.label)

    def pull(self, num):
        """

        :rtype: :class:`PullRequest`
        """

        pull = self.make(PullRequest, self, num)
        return pull.sync()

    def issue(self, num):
        """
        :rtype: :class:`Issue`
        """
        return self.make(Issue, self, num).sync()

    def ref(self, ref):
        """
        :rtype: :class:`Reference`
        """
        return self.make(Reference, self, ref)

    def merge(self, base, head, message):
        """Perform a merge.

        See also:
            https://developer.github.com/v3/repos/merging/#perform-a-merge
        """
        return self.client.request(
            "{}/merges".format(self.base_path),
            params={
                "base": base,
                "head": head,
                "commit_message": message
            }, method="POST")

    def create_pull(self, title, head, base, body,      # pylint: disable=R0913
                    maintainer_can_modify=False):
        """Create a pull reuqest."""
        pull = self.make(PullRequest, self, 0)
        pull.title = title
        pull.head = head
        pull.base = base
        pull.body = body
        pull.maintainer_can_modify = maintainer_can_modify
        return pull.create()

    def create_issue(self, title, body,     # pylint: disable=R0913
                     milestone=None, labels=None, assignees=None):
        """Create an issue."""
        issue = self.make(Issue, self, 0)
        issue.title = title
        issue.body = body
        issue.milestone = milestone
        issue.labels = labels
        issue.assignees = assignees
        return issue.create()

    def create_status(self, sha, state, **kwargs):
        """Create a status

        See also:
            https://developer.github.com/v3/repos/statuses/#create-a-status
        """
        state = StatusState(state)
        params = {
            "state": state.value,
        }

        params.update(kwargs)

        return self.client.request(
            self.base_path + "/statuses/" + sha, params=params, method="POST")

    def get_statuses(self, sha):
        """Returns statuses for a specific SHA.

        See also:
            https://developer.github.com/v3/repos/statuses/#list-statuses-for-a-specific-ref
        """
        return self.client.request(
            self.base_path + "/commits/" + sha + "/statuses")
