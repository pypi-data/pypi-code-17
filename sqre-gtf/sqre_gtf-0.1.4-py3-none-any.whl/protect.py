from codekit import codetools


def protect(github_repo, branch_name='master', verbose=False):
    branch = github_repo.branch(branch_name)
    if branch.protected:
        if verbose:
            print('[{0}/{1}] ({2}) branch is already protected.'.format(
                github_repo.owner.login, github_repo.name,
                branch_name))
    else:
        codetools.protect(github_repo, branch_name)
        if verbose:
            print('[{0}/{1}] ({2}) branch is protected.'.format(
                github_repo.owner.login, github_repo.name,
                branch_name))
