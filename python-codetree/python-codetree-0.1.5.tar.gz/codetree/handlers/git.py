import logging
import os
from six.moves.urllib.parse import urlparse
import shutil
from subprocess import (
    check_output,
    CalledProcessError,
    STDOUT
)

from .basic import HandlerResult, SourceHandler
from .exceptions import NotABranch, NotSameBranch, InvalidOption
from .utils import log_failure


class GitSourceHandler(SourceHandler):
    """Check out a git working tree"""

    schemes = (
        "git",
        "git+http",
        "git+https",
        "git+ssh",
    )

    def __init__(self, source):
        super(GitSourceHandler, self).__init__(source)
        scheme = urlparse(source).scheme
        # strip git+ from the source
        if scheme in ("git+http", "git+https", "git+ssh"):
            self.source = source[4:]
        else:
            self.source = source

    def check_and_update(self, dest):
        """ Verify the current checkout at dest and fetch latest changes
        :param dest: Destination for the repository
        :return: True on success
        """
        # Verify the current checkout is the right branch
        if not os.path.isdir(os.path.join(dest, '.git')):
            raise NotABranch('{} is not a git repository'.format(dest))
        origin = self._git_config(dest, 'remote.origin.url')
        if origin != self.source:
            raise NotSameBranch("{} failed: origin is {} not {}.".format(dest, origin, self.source))

        # fetch latest
        if not log_failure(self._git_cmd(dest, 'fetch'), None):
            return False

        # If needed merge
        try:
            full_ref = check_output(self._git_cmd(dest, 'symbolic-ref', '-q', 'HEAD'), universal_newlines=True).strip()
        except CalledProcessError:
            full_ref = ''
        if full_ref:
            upstream_ref = check_output(self._git_cmd(dest, 'for-each-ref', '--format=%(upstream)', full_ref), universal_newlines=True).strip()
            if upstream_ref:
                if not log_failure(self._git_cmd(dest, 'merge', '--ff-only', upstream_ref),
                                   "Updating repository at {} from {}".format(dest, upstream_ref)):
                    return False

        return True

    def get(self, dest, options):
        result = HandlerResult(False, source=self.source_raw, dest=dest, options=options)
        ref = options.get('revno')
        depth = options.get('depth')
        branch = options.get('branch')
        if branch and ref:
            raise InvalidOption("revno and branch")

        clone_command = ['git', 'clone', self.source, dest]
        if depth:
            d = int(depth)
            clone_command.extend(["--depth", str(d)])
        if branch:
            clone_command.extend(["--single-branch", "-b", str(options.get("branch"))])
        if os.path.exists(dest):
            if options.get("overwrite"):
                shutil.rmtree(dest)
                if not log_failure(clone_command,
                                   "Cloning repository at {} from {}".format(dest, self.source)):
                    return result
            else:
                if not self.check_and_update(dest):
                    return result
                if ref is None:  # default to master for the checkout of any updated repo
                    ref = 'master'
        else:
            if not log_failure(clone_command,
                               "Cloning repository at {} from {}".format(dest, self.source)):
                return result

        # Checkout the ref if one was specified
        if ref is not None:
            if not log_failure(self._git_cmd(dest, 'checkout', ref), None):
                return result

        revision = check_output(self._git_cmd(dest, 'rev-parse', 'HEAD'), stderr=STDOUT, universal_newlines=True).strip()
        if ref is not None:
            logging.info("Repository {} at ref {} revision {}".format(dest, ref, revision))
        else:
            logging.info("Repository {} at revision {}".format(dest, revision))

        result.success = True
        result.revision = revision
        return result

    @staticmethod
    def _git_cmd(dest, *args):
        cmd = ['git', '-C', dest]
        cmd.extend(args)
        return cmd

    def _git_config(self, dest, key):
        try:
            return check_output(self._git_cmd(dest, 'config', key), universal_newlines=True).strip()
        except CalledProcessError:
            return ''
