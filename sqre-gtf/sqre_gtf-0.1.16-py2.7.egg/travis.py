from codekit import codetools

from .base import token


def travis(github_repo, verbose=False):
    success = codetools.enable_travisci(github_repo, token())
    if verbose:
        print('Travis CI webhook enabled for [{0}/{1}].'.format(
            github_repo.owner.login, github_repo.name))
    return success
