# Copyright (C) 2017 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python interface to Git.

The main member of this module is the git() generic function.

The most general git() method is for GitEnv instances, which describes a
Git invocation environment.

Most users can use the string git() method, which will be interpreted as
the working tree for a standard non-bare Git repo.

If you have your own Git wrappers, you can register a git() method for
it so git() can accept them as environments transparently.

Members:

git() -- All-purpose generic function interface to Git
GitEnv -- Git invocation environment
has_unpushed_changes()
has_staged_changes()
has_unstaged_changes()
"""

import functools
from pathlib import Path
import subprocess

__version__ = '1.0.0'


class GitEnv:

    """Environment for Git invocations."""

    def __init__(self, gitdir: 'PathLike', worktree: 'PathLike'):
        self.gitdir = Path(gitdir).expanduser()
        self.worktree = Path(worktree).expanduser()


@functools.singledispatch
def git(env, args, **kwargs):
    """Run a Git command.

    env is a Git environment, or some representation of a Git
    environment.  args and kwargs are passed to subprocess.run().

    Additional methods should be implemented by creating a suitable
    GitEnv instance and calling git() again with it.

    Returns a CompletedProcess.
    """
    raise NotImplementedError


@git.register(GitEnv)
def _git_gitenv(env, args, **kwargs):
    return subprocess.run(
        ['git', '--git-dir', str(env.gitdir),
         '--work-tree', str(env.worktree), *args],
        **kwargs)


@git.register(str)
def _git_str(worktree, args, **kwargs):
    env = GitEnv(gitdir=Path(worktree) / '.git',
                 worktree=worktree)
    return git(env, args, **kwargs)


def has_unpushed_changes(env):
    """Return True if the Git repo has unpushed changes."""
    result = git(env, ['rev-list', '-n', '1', 'HEAD@{u}..HEAD'],
                 stdout=subprocess.PIPE)
    return bool(result.stdout)


def has_staged_changes(env):
    """Return True if the Git repo has staged changes."""
    result = git(env, ['diff-index', '--quiet', '--cached', 'HEAD'])
    return result.returncode != 0


def has_unstaged_changes(env):
    """Return True if the Git repo has unstaged changes."""
    result = git(env, ['diff-index', '--quiet', 'HEAD'])
    return result.returncode != 0
