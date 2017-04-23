import os
import re
import github
import github.GithubObject
import json
import yaz

from .version import __version__
from .spreadsheet import VersionMatrixSheet
from .github import Github
from .log import logger, set_verbose

__all__ = ["DependencyMatrix", "GithubFinder"]


class DependencyMatrix(yaz.BasePlugin):
    json_key_file = None
    sheet_key = None

    def __init__(self):
        if not (self.json_key_file and self.sheet_key):
            raise RuntimeError("The json_key_file and sheet_key must be specified, please add a DependencyMatrix plugin override in your user directory")

    @yaz.dependency
    def set_github(self, github: Github):
        self.github = github.get_service()

    @yaz.task
    def version(self, verbose: bool = False):
        set_verbose(verbose)
        return __version__

    @yaz.task
    def update_spreadsheet(self, limit: int = 666, verbose: bool = False):
        set_verbose(verbose)

        sheet = VersionMatrixSheet(os.path.expanduser(self.json_key_file), self.sheet_key)
        sheet.set_updating()
        try:
            for repo in self.get_repos()[:limit]:
                dependencies = self.get_dependencies(repo)
                if dependencies:
                    sheet.set_dependencies(repo, dependencies)
        finally:
            sheet.unset_updating()

    def get_repos(self):
        return self.github.get_user().get_repos()

    def get_dependencies(self, repo, ref=github.GithubObject.NotSet):
        try:
            file = repo.get_file_contents('/composer.lock', ref)
        except github.GithubException:
            return {}
        data = json.loads(file.decoded_content.decode())

        return {package['name']: package['version'].strip() for package in data['packages']}

class GithubFinder(yaz.BasePlugin):
    @yaz.dependency
    def set_github(self, github: Github):
        self.github = github.get_service()

    @yaz.task
    def search(self, pattern: str, filename: str = "/README.md", verbose: bool = False):
        set_verbose(verbose)
        exp = re.compile(pattern)

        for repo in self.github.get_user().get_repos():
            try:
                file = repo.get_file_contents(filename)
            except github.GithubException:
                logger.debug("%s: no file found", repo.name)
                continue

            content = file.decoded_content.decode()
            if exp.search(content):
                print(repo.name)
            else:
                logger.debug("%s: no match found", repo.name)

