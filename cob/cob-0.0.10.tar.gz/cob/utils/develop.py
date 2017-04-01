import os
import subprocess

_COB_DEVELOP_MODE = 'COB_DEVELOP'


def is_develop():
    return _COB_DEVELOP_MODE in os.environ


def cob_root():
    assert is_develop()
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def cob_branch():
    git = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cob_root(), stdout=subprocess.PIPE)
    git.check_returncode()
    return git.stdout.decode("UTF-8").strip()
