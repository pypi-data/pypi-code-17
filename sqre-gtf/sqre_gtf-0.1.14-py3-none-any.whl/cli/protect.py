#!/usr/bin/env python
from gtf.base import get_parser, get_repos
from gtf.protect import protect


def main():
    parser = get_parser('Enable default Github branch protection.')
    parser.add_argument('-b', '--branch_name', default='master',
                        help='The branch name to protect. Defaults'
                        ' to master.')
    args = parser.parse_args()
    for r in get_repos(args):
        protect(r, args.branch_name, args.verbose)


if __name__ == '__main__':
    main()
