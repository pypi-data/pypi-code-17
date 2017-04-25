import os
import sys
from urlparse import urljoin

import requests


def upload():
    url = urljoin(
        os.environ['LINTER_URL'], '/repos/{repo}/statuses/{sha}'
    ).format(
        repo=os.environ['TRAVIS_REPO_SLUG'],
        sha=os.environ['TRAVIS_PULL_REQUEST_SHA']
    )

    requests.post(
        url,
        sys.stdin.read()
    )

