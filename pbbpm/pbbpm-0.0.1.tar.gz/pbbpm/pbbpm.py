"""
Python BitBucket Package Manager.
"""
import sys
import pip

__all__ = ['main']


def main(args):
    data = args
    data.remove('-m')
    if '--upgrade' not in data:
        data.insert(1, '--upgrade')
    if 'https://bitbucket.org/' not in data[2]:
        data[2] = data[2].replace(data[2], 'https://bitbucket.org/' + data[2])
    if 'git+' not in data[2]:
        data[2] = data[2].replace(data[2], 'git+' + data[2])
    if '.git' not in data[2]:
        data[2] = data[2].replace(data[2], data[2] + '.git')
    pip.main(data)


main(sys.argv)
