"""
This Module provides utilities to gain a pass/fail exit status based on pylint
scores and acceptable conditions for pylint files

Using lint() with a list of file names as an argument will run pylint on each
python file in the list, create a results dictionary, and return a numeric exit
code
"""
import logging
import argparse
import sys
import subprocess
import pathlib
import re

### Logging Initialization
LOGGER = logging.getLogger(__name__)
FORMATTER = logging.Formatter('{levelname}---{module:->20}.{funcName:-<20}---{message}', style='{')

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)

'''
### Argument Parsing Initialization
PARSER = argparse.ArgumentParser(description='Utility to add Pass/Fail output on top of Pylint for version management purposes')
PARSER.add_argument('-v', '--verbosity',
                    metavar='LEVEL',
                    help='Specify level of verbosity for output',
                    type=int,
                    choices=range(0, 6),
                    default=2
)
PARSER.add_argument('target',
                    help='Specify a target on which the program will be run',
                    type=str,
                    nargs='*',
                    default=['.']
)
PARSER.add_argument('-e', '--exclude',
                    help='Specify errors for pylint to ignore',
                    type=str,
                    nargs='*',
                    default=['']
)
PARSER.add_argument('-i', '--ignore', # Maybe add a .pylintignore file to read
                    help='Specify files to ignore',
                    type=str,
                    nargs='*',
                    default=['']
)
TARGET_GROUP = PARSER.add_mutually_exclusive_group(required=True)
TARGET_GROUP.add_argument('-g', '--git',
                          help='Process target as an option for git diff',
                          type=str,
                          nargs='?',
                          choices=['STAGED', 'LAST'],
                          const='LAST',
                          action='store',
                          dest='target_type'
)
TARGET_GROUP.add_argument('-f', '--filename',
                          help='Process target as a filename or list of filenames',
                          action='store_const',
                          const='FILE',
                          dest='target_type'
)
TARGET_GROUP.add_argument('-d', '--dirname',
                          help='Process target as a directory or list of directories',
                          action='store_const',
                          const='DIR',
                          dest='target_type'
)
'''

### Default Comparison Values
MINIMUM_ALLOWED_SCORE  = 7.00
MAXIMUM_ALLOWED_ERRORS = 0

def _parse_git_diff(git_diff):
    file_list = []
    LOGGER.debug('Files from diff: %s', git_diff)
    file_list = re.findall('^(.*)$', git_diff, re.MULTILINE)
    return file_list

def _parse_pylint(pylint_report):
    results = {}
    results['Report'] = {}
    score = re.findall(r'Your code has been rated at ([-0-9.]*)/10\s', pylint_report)
    # the above regex returns the score as a string in a list and could be empty
    LOGGER.debug('regex matches: %s', score)
    assert score, 'Bad pylint report'
    score = float(score[0])
    error_report = re.findall(r'(^E:\s*\d*,\s*\d*:.*$)', pylint_report, re.MULTILINE)
    warning_report = re.findall(r'(^W:\s*\d*,\s*\d*:.*$)', pylint_report, re.MULTILINE)
    convention_report = re.findall(r'(^C:\s*\d*,\s*\d*:.*$)', pylint_report, re.MULTILINE)
    errors = len(error_report)
    warnings = len(warning_report)
    conventions = len(convention_report)
    LOGGER.debug('score: %s', score)
    LOGGER.debug('errors: %s', errors)
    LOGGER.debug('warnings: %s', warnings)
    LOGGER.debug('conventions: %s', conventions)
    results['Score'] = score
    results['Errors'] = errors
    results['Warnings'] = warnings
    results['Conventions'] = conventions
    results['Report']['Errors'] = error_report
    results['Report']['Warnings'] = warning_report
    results['Report']['Conventions'] = convention_report
    return results

def _shell_git_diff(diff_option):
    LOGGER.debug('diff_option: %s', diff_option)
    if diff_option == 'STAGED':
        shell_option = '--cached'
    elif diff_option == 'LAST':
        shell_option = 'HEAD~1 HEAD'
    command = 'git diff {} --name-only'.format(shell_option)
    with open('./.git-diff.outp', 'w') as output_file:
        subprocess.call(command, shell=True,
                        stdout=output_file,
                        stderr=output_file
        )
    with open('./.git-diff.outp', 'r') as output_file:
        output = output_file.read()
    LOGGER.debug('git diff output: {}'.format(output))
    return output

def _shell_pylint(path, excludes):
    if isinstance(path, pathlib.Path):
        filename='/'.join(path.parts)
    command = 'pylint3 {}'.format(filename)
    with open('./.pylint.outp', 'w') as output_file:
        subprocess.call(command, shell=True,
                        stdout=output_file,
                        stderr=output_file
        )
    with open('./.pylint.outp', 'r') as output_file:
        output = output_file.read()
    return output

def _lint_file(path_obj, excludes=''):
    """***VERY CRUDE***
        pylint does have an importable python package but the documentation for
        using it is scarce at best. This function could be improved if it used
        pylint's actual python functionality
    ***************************************************************************
    Creates a results dictionary for a specified file
        Args: path_obj - expects a pathlib.Path object
              excludes - errors to exclude
        Rtrn: results  - dictionary of files and their results
    """
    LOGGER.debug('Args: %s', path_obj)
    assert isinstance(path_obj, pathlib.Path)
    LOGGER.info('Linting File: "%s"...', path_obj.name)
    results = {}
    output = _shell_pylint(path_obj, excludes)
    results[path_obj.name] = _parse_pylint(output)
    return results

def _list_git(target, ignores=['']):
    """***VERY CRUDE***
        Currently this function opens a shell subprocess to run git diff;
        there is a git python libraryi, GitPython (importable as git), that
        could be used to improve the code
    ***************************************************************************
    Generates a list of pathlib.Path objects representing python files
        Args:
            target ---- a list with a single element 'LAST' or 'STAGED'
            ignores --- a list of paths to ignore
        Returns:
            file_list - list of pathlib.Path objects
    """
    LOGGER.debug('diff_option: %s', target)
    file_list = []
    assert target == 'STAGED' or target == 'LAST'
    output = _shell_git_diff(target)
    diff_list = _parse_git_diff(output)
    for item in diff_list:
        path_obj = pathlib.Path(item)
        if path_obj.is_file() and path_obj.suffix == '.py':
            file_list.append(path_obj)
            LOGGER.debug('added: %s', path_obj.name)
        else:
            LOGGER.debug('ignored: %s', path_obj.name)
    return file_list

def _list_dir(target, ignores=['']):
    """Generates a list of pathlib.Path objects representing python files
        Args:
            target ---- expects a list of valid directories
            ignores --- a list of paths to ignore
        Returns:
            file_list - list of pathlib.Path objects
    """
    LOGGER.debug('dir: %s', target)
    file_list = []
    assert isinstance(target, list), 'Expected list'
    for _dir in target:
        dir_obj = pathlib.Path(_dir)
        if dir_obj.is_dir():
            for path_obj in dir_obj.iterdir():
                if path_obj.is_file() and path_obj.suffix == '.py':
                    file_list.append(path_obj)
                    LOGGER.debug('added: %s', '/'.join(path_obj.parts))
                else:
                    LOGGER.debug('ignored: %s', '/'.join(path_obj.parts))
        else:
            LOGGER.error('Invalid directory: %s', dir_obj.name)
    return file_list

def _list_files(target, ignores=['']):
    """Generates a list of pathlib.Path objects representing python files
        Args:
            target ---- expects a list of valid files
            ignores --- a list of paths to ignore
        Returns:
            file_list - list of pathlib.Path objects
    """
    LOGGER.debug('file(s): %s', target)
    assert isinstance(target, list), 'Expected list'
    file_list = []
    for file_ in target:
        path_obj = pathlib.Path(file_)
        assert path_obj.is_file, 'Invalid file: {}'.format(path_obj.name)
        if path_obj.suffix == '.py':
            file_list.append(path_obj)
            LOGGER.debug('added: %s', path_obj.name)
        else:
            LOGGER.debug('ignored: %s', path_obj.name)
    return file_list

def _print_results(filename, results):
    """
    Prints results out in the form:
    <filename>
    |__Score : <pylint-score>
    |__Errors: <pylint-error-count>
    |__Report:
    |____Errors:
    |______...
    |____Warnings:
    |______...
    |____Conventions:
    |______...
    ...

    depending on the verbosity of LOGGER
    """
    logging_level = LOGGER.getEffectiveLevel()
    LOGGER.debug('logging level: %s', logging_level)
    if logging_level >= 50:
        return
    else:
        print('\n{}:'.format(filename))
        print('|__Score   : {}'.format(results['Score']))
        print('|__Errors  : {}'.format(results['Errors']))
        print('|__Warnings: {}'.format(results['Warnings']))
        print('|__Conventions: {}'.format(results['Conventions']))
        print('|__Report:')
        print('|____Errors:')
        for error in results['Report']['Errors']:
            print('|_______{}'.format(error))
        if logging_level < 40:
            print('|____Warnings:')
            for warning in results['Report']['Warnings']:
                print('|_______{}'.format(warning))
        if logging_level < 30:
            print('|____Conventions:')
            for convention in results['Report']['Conventions']:
                print('|_______{}'.format(convention))

def check_results(results):
    """
    Check results dictionary for files that do not meet the standard specified
    by the constants:
        MAXIMUM_ALLOWED_ERRORS
        MINIMUM_ALLOWED_SCORE
    Also calls _print_results()
    """
    LOGGER.debug('Args: %s', results)
    bad_files = []
    exit_status = 0
    for filename, results in results.items():
        _print_results(filename, results) # print is based off LOGGER.level
        test_error = results['Errors'] > MAXIMUM_ALLOWED_ERRORS
        test_score = results['Score'] <= MINIMUM_ALLOWED_SCORE
        if test_error or test_score:
            exit_status+= 1
            LOGGER.info('%s: failed', filename)
            bad_files.append(filename)
        else:
            LOGGER.info('%s: passed', filename)
            continue
    if LOGGER.getEffectiveLevel() <= 50:
        if exit_status != 0:
            print('\n\nFAILED\n')
            print(bad_files)
        else:
            print('\n\nPASSED\n')
    return exit_status

def evaluate_target(target, target_type='FILE'):
    """Turns target into a set of python files to be linted
        CATCHES:
            AssertionError ---- raised by _list*() functions when they encounter
                                targets not correctly specified
        Args:
            target ------ a list of arguments
            target_type - how the argument will be handled:
                LAST | STAGED - will run a git diff of the current directory
                DIR ----------- will iterate though directories given in target
                FILE ---------- will iterate though files given in target
        Returns:
            file_list --------- list of pathlib.Path objects representing
                                python files
    """
    LOGGER.debug('target: %s', target)
    LOGGER.debug(': %s', target_type)
    file_list = []
    try:
        if target_type == 'LAST' or target_type == 'STAGED':
            file_list = _list_git(target_type)
        elif target_type == 'DIR':
            file_list = _list_dir(target)
        elif target_type == 'FILE':
            file_list = _list_files(target)
        else:
            LOGGER.error('Invalid "target_type": %s', target_type)
            file_list = None
    except AssertionError as error:
        LOGGER.error(error)
        file_list = None
    return file_list

def lint(path_list, excludes=''):
    """Runs pylint on all files in path list and returns results dictionary
        CATCHES:
            AssertionError - raised or thrown by _lint_file due to unexpected
                pylint output
        Args:
            path_list ------ a list of pathlib.Path objects representing python
                files
            excludes ------- a list of Errors for pylint to ignore
        Returns:
            results -------- a dict of the files and reports for each
    """
    results = {}
    for path in path_list:
        try:
            _entry = _lint_file(path, excludes)
            results.update(_entry)
        except AssertionError as error:
            LOGGER.error('Error encountered for %s %s', path, error)
    return results

def main(target, target_type, excludes=[''], ignore=['']):
    LOGGER.debug('Args: %s', target)
    exit_status = 0
    file_list = evaluate_target(target, target_type)
    assert file_list or target_type != 'FILE', 'No python files in target'
    if file_list:
        results = lint(file_list, excludes)
        exit_status = check_results(results)
    else:
        LOGGER.warning('No python files found in target')
    return exit_status

if __name__ == '__main__':
    # Argument parsing
    ARGS = PARSER.parse_args()
    TARGET      = ARGS.target
    TARGET_TYPE = ARGS.target_type
    VERBOSITY   = (5-ARGS.verbosity)*10
    ###FIXME: add support for excluded errors
    ###FIXME: add support for files to ignore
    EXCLUDES = ''
    # Global variable setting
    LOGGER.setLevel(VERBOSITY)
    LOGGER.debug('cmd line args %s', ARGS)
    # Execution
    try:
        EXIT_CODE = main(TARGET, TARGET_TYPE, EXCLUDES)
    except AssertionError as error:
        LOGGER.critical(error)
        EXIT_CODE = -1
    sys.exit(EXIT_CODE)

# File:   pylint_ci.py
# Author: Andrew Dehel

