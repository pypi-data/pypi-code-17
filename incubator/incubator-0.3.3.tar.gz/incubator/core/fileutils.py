"""
Utility methods using for files and archives manipulation and filtering.
"""
import fnmatch
import logging
import os

from .constants import APP_NAME, FILE_MODE_FROM_URL

logger = logging.getLogger(APP_NAME)


def match_filters(file, patterns):
    for p in patterns:
        if fnmatch.fnmatchcase(file, p):
            return True
    return False


def filter_files(files, patterns):
    filtered_files = []

    for f in files:
        if match_filters(f, patterns):
            filtered_files.append(f)
    return filtered_files


def get_filtered_files(files, patterns, tar):
    root_dirs = []

    filtered_objects = set([])
    for f in files:
        if match_filters(f, patterns):
            fi = tar.getmember(f)
            if fi.isfile():
                filtered_objects.add(f)
            elif fi.isdir():
                root_dirs.append(f)

    root_dirs.sort(key=len)
    for d in root_dirs:
        pattern = "{}{}*".format(d.split(os.sep)[-1],
                                 os.sep)
        matched_subfiles = filter_files(files, [pattern])
        if len(matched_subfiles) == 0:
            if len(d.split(os.sep)) > 1:  # empty subdirectory
                filtered_objects.add(d)
        else:
            filtered_objects.update(matched_subfiles)
            for subfile in matched_subfiles:
                if subfile in root_dirs:
                    root_dirs.remove(subfile)
    return filtered_objects


def change_tarinfo_properties(tarinfo):
    """
    Filter for insertion local file to tar archive.
    :param tarinfo: tarinfo to insert
    :return: original tarinfo with changed permissions
    """
    tarinfo.uid = 0
    tarinfo.gid = 0
    return tarinfo


def change_tarinfo_properties_mode(tarinfo):
    """
    Filter for insertion not-local file to tar archive.
    :param tarinfo: tarinfo to insert
    :return: original tarinfo with changed permissions
    """
    tarinfo.uid = 0
    tarinfo.gid = 0
    tarinfo.mode = FILE_MODE_FROM_URL
    return tarinfo


def normalise_patterns(patterns):
    normpattern = []
    for p in patterns:
        normpattern.append(os.path.normpath(p))
    return normpattern


def remove_top_parent(path):
    return os.sep.join(path.split(os.sep)[1:])


def is_top_file(path):
    return len(path.split(os.sep)) > 1


def put_archive(client, config, container, tar, target):
    logger.debug('------> creating target folder:\n{}'.format(target))
    create_directory(client, config, container, target)
    client.put_archive(container=container,
                       path=target,
                       data=tar.getvalue())


def create_directory(client, config, container, target):
    client.execute(container=container,
                   cmd=config.mkdir_command + ' {}'.format(
                       target))


def copy_files_to_container(container, client, config, context, source, target):
    single_file = None
    if target != os.curdir and target[-1] != os.path.sep:  # destination is file
        single_file = os.path.basename(target)
        target = os.path.dirname(os.path.join(os.curdir, target))

    tar = context.get_archive(patterns=source,
                              single_file=single_file)

    if not tar:
        logger.warning('------> nothing to copy\n{}'.format(target))
        return

    put_archive(client, config, container, tar, target)


def norm_path_with_work_dir(path, workdir):
    if not workdir:
        return path

    has_sep = path[-1] == os.sep
    return_path = os.path.normpath(os.path.join(workdir, path))
    if has_sep:
        return_path += os.sep
    return return_path
