import logging
import os
import re
import shutil
from subprocess import (
    check_output,
    CalledProcessError,
    check_call,
)
from six.moves.urllib.parse import urlparse

from .basic import HandlerResult, SourceHandler
from .exceptions import BranchDiverged, NotABranch
from .utils import log_failure, strip_trailing_slash


class BzrSourceHandler(SourceHandler):
    """Check out a bazaar working tree"""

    schemes = (
        "bzr",
        "bzr+ssh",
        "lp",
        "bzr+http",
        "bzr+https",
        "nosmart+bzr",
        "nosmart+bzr+ssh",
        "nosmart+lp",
    )

    def __init__(self, source):
        super(BzrSourceHandler, self).__init__(source)
        scheme = urlparse(source).scheme
        if scheme in ("bzr+http", "bzr+https"):
            # Strip 'bzr+'.
            self.source = source[4:]
        else:
            self.source = source
        self.dest_source = "unset"

    def _set_parent(self, dest):
        cmd = ['bzr', 'config', '-d', dest, 'parent_location={}'.format(self.source)]
        return log_failure(cmd, "Setting repository parent to {}.".format(self.source))

    def has_lp_auth(self):
        return os.path.exists(os.path.join(os.environ['HOME'],
                                           '.bazaar/authentication.conf'))

    def checkout_branch(self, dest, options):
        parent_dir = os.path.dirname(dest)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        lightweight = options.get('lightweight', '')
        cmd = ['bzr']
        if lightweight.lower() in ('true', 't', '1'):
            cmd.append('checkout')
            cmd.append('--lightweight')
            msg = "Checking out {} to {}"
        else:
            cmd.append('branch')
            msg = "Branching {} to {}"
        if options.get('revno'):
            cmd.append('-r')
            cmd.append(options.get('revno'))
        cmd = cmd + [self.source, dest]
        return log_failure(cmd, msg.format(self.source, dest))

    def update_branch(self, dest):
        cmd = ['bzr', 'update', dest]
        return log_failure(cmd, "No revno specified: Updating {} to tip".format(dest, self.source))

    def pull_branch(self, dest, options):
        cmd = ["bzr", "pull"]
        if options.get('overwrite'):
            cmd.append('--overwrite')
        if options.get('revno'):
            cmd.append('-r')
            cmd.append(options.get('revno'))
        cmd = cmd + ["-d", dest]
        return log_failure(cmd, "Pulling {} from parent ({})".format(dest, self.source))

    def revno_branch(self, dest, revno):
        cmd = ['bzr', 'update', '-r', revno, dest]
        return log_failure(cmd, "Checking out revision {} of {}".format(revno, self.source))

    def parent_branch(self, branch, local=False):
        bzr_cmd = ("bzr", "info", "-q", branch)
        output = check_output(bzr_cmd, universal_newlines=True)
        # 'repository branch' has higher relevance than 'branch root', e.g:
        # m_repo:   bzr info lp:charms/trusty/ceph
        # m_root:   bzr info lp:mojo
        # m_parent: bzr info /path/to/local/branch
        m_repo = m_root = m_parent = None
        if local:
            m_parent = re.match(r".*parent branch: (\S+)", output, re.MULTILINE | re.DOTALL)
        else:
            m_repo = re.match(r".*repository branch: (\S+)", output, re.MULTILINE | re.DOTALL)
            m_root = re.match(r".*branch root: (\S+)", output, re.MULTILINE | re.DOTALL)
        match = m_repo or m_root or m_parent
        if match:
            parent = match.group(1)
            parent = strip_trailing_slash(parent)
            return parent
        else:
            return None

    def normalize_lp_branch(self, branch):
        if branch.startswith(('lp:', 'nosmart+lp:')):
            if self.has_lp_auth():
                if '~' not in branch:
                    branch = branch.replace('lp:', 'lp:+branch/')
                branch = branch.replace('lp:', 'bzr+ssh://bazaar.launchpad.net/')
            else:
                # properly map lp: to http://bazaar.launchpad.net/...
                # for anon branching
                branch = self.parent_branch(branch)
        return branch

    def is_same_branch(self, dest):
        if not self.is_bzr_branch(dest):
            raise NotABranch("{} is not a bzr branch".format(dest))
        self.source = strip_trailing_slash(self.source).strip()
        self.source = self.normalize_lp_branch(self.source)
        self.dest_source = self.parent_branch(dest, True)
        return self.dest_source == self.source

    def is_bzr_branch(self, branch):
        branch = self.normalize_lp_branch(branch)
        bzr_cmd = ("bzr", "revno", branch)
        devnull = open('/dev/null', 'w')
        try:
            check_call(bzr_cmd, stdout=devnull)
            return True
        except CalledProcessError as e:
            if e.returncode == 3:
                # Try bzr info instead of bzr revno, which fails on some
                # branches per lp bug#1161018
                bzr_cmd = ("bzr", "info", branch)
                try:
                    check_call(bzr_cmd, stdout=devnull)
                    return True
                except CalledProcessError as e:
                    if e.returncode == 3:
                        return False
                    else:
                        raise e
            else:
                raise e

    def get_branch_revno(self, branch):
        """Return the branch revno"""
        cmd = ['bzr', 'revno', branch]
        return check_output(cmd, universal_newlines=True).strip()

    def get_working_tree_revno(self, branch):
        """Return the working tree revno"""
        cmd = ['bzr', 'version-info', branch]
        output = check_output(cmd, universal_newlines=True).split('\n')
        for line in output:
            if line.startswith('revno:'):
                line = line.strip()
                return line.split()[1]

    def check_and_update(self, dest, options):
        """ Update a branch if needed
        :dest: Destination directory
        :options: Dictionary of options for this directive
        :return: True is successful
        """
        # Pull from parent
        if not self.pull_branch(dest, options):
            raise BranchDiverged("{} failed: has diverged from {}".format(dest, self.source))
            return False
        # Handle downgrading
        if options.get("revno") and not options.get("overwrite"):
            # Update only if working tree does not match
            # requested revno
            if not self.get_working_tree_revno(dest) == options.get("revno"):
                if not self.revno_branch(dest, options.get("revno")):
                    return False
        # Handle upgrade from previously downgraded
        # working tree not at tip on disk
        if not options.get("revno"):
            # Update only if working tree is not at tip
            if not self.working_tree_matches_revno(dest):
                if not self.update_branch(dest):
                    return False
        return True

    def working_tree_matches_revno(self, branch):
        """Compare working tree revno against branch revno
           return True or False"""
        return self.get_branch_revno(branch) == self.get_working_tree_revno(branch)

    def get(self, dest, options):
        result = HandlerResult(False, source=self.source_raw, dest=dest, options=options)
        if not self.is_bzr_branch(self.source):
            raise NotABranch("{} is not a bzr branch. Is it a private branch? Check permissions on the branch.".format(self.source))
        if os.path.exists(dest):
            # if the parent is the same, update the branch
            if self.is_same_branch(dest):
                if not self.check_and_update(dest, options):
                    return result
            elif options.get("overwrite"):
                logging.info("Overwriting {}".format(dest))
                shutil.rmtree(dest)
                if not self.checkout_branch(dest, options):
                    return result
            else:
                logging.warn("Warning: {}'s parent is {} not {}.".format(dest, self.dest_source, self.source))
                self._set_parent(dest)
                if not self.check_and_update(dest, options):
                    return result
        else:
            if not self.checkout_branch(dest, options):
                return result

        revno = self.get_working_tree_revno(dest)
        logging.info("{} is at revno {}".format(dest, revno))

        result.success = True
        result.revision = revno
        return result
