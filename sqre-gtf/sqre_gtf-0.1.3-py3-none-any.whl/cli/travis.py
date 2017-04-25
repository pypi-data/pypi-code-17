#!/usr/bin/env python
from gtf.base import get_parser, get_repos
from gtf.travis import travis


def main():
    parser = get_parser('Enable TravisCI webhook for repository(ies).')
    args = parser.parse_args()
    repos = get_repos(args)
    for r in repos:
        travis(r, args.verbose)


if __name__ == '__main__':
    main()
