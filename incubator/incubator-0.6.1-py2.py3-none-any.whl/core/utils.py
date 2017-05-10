"""
Utility methods for builder.
"""
import collections
import io
import logging
import os
import re
import string
import tarfile
import tempfile

import six

from .constants import (APP_NAME, CONTEXT_FILE_IN_MEMORY, CONTEXT_FILE_ON_DISK,
                        DEFAULT_CONTEXT_FILE_LIMIT)
from .output import CHAPTER

logger = logging.getLogger(APP_NAME)


def dockerfile_from_context(context, path):
    with tarfile.open(mode="r", fileobj=context) as t:
        df = t.extractfile(t.getmember(path))
    dockerfile = six.BytesIO()
    dockerfile.writelines(df.readlines())
    dockerfile.seek(0)
    context.seek(0)
    return dockerfile


def mkbuildcontext(path, fileobj, custom_context, dockerfile, client, limit=None):
    if path is None and fileobj is None:
        raise TypeError("Either path or fileobj needs to be provided.")

    dockerfile = dockerfile or "Dockerfile"

    if custom_context:
        if not fileobj:
            raise TypeError("You must specify fileobj with custom_context")
        return fileobj, dockerfile_from_context(fileobj, dockerfile)
    elif fileobj is not None:
        return make_build_context_from_dockerfile(fileobj), fileobj
    elif path.startswith(('http://', 'https://',
                          'git://', 'github.com/', 'git@')):
        # TODO
        return None, None
    elif not os.path.isdir(path):
        raise TypeError("You must specify a directory to build in path")
    else:
        dockerignore = os.path.join(path, '.dockerignore')
        exclude = None
        if os.path.exists(dockerignore):
            with open(dockerignore, 'r') as f:
                exclude = list(filter(bool, f.read().splitlines()))
        context = tar(
            path, client, exclude=exclude, dockerfile=dockerfile, limit=limit
        )
        dockerfile_obj = dockerfile_from_context(context=context, path=dockerfile)
        return context, dockerfile_obj


def exclude_paths(root, exclude, dockerfile, client):
    files = client.exclude_paths_from_context(root, exclude, dockerfile)
    return files


def tar(path, client, exclude=None, dockerfile=None, fileobj=None, limit=DEFAULT_CONTEXT_FILE_LIMIT):
    if not fileobj:
        fileobj = tempfile.SpooledTemporaryFile(max_size=limit)

    root = os.path.abspath(path)
    exclude = exclude or []

    logger.debug(CHAPTER.format("context:"))
    with tarfile.open(mode='w', fileobj=fileobj) as t:
        for p in sorted(exclude_paths(root, exclude,
                                      dockerfile=dockerfile,
                                      client=client)):
            logger.debug("- {}".format(p))
            t.add(name=os.path.join(path, p), arcname=p)
    logger.debug("")
    fileobj.seek(0)

    if isinstance(fileobj, tempfile.SpooledTemporaryFile):
        if fileobj.name:
            context_file_type = CONTEXT_FILE_ON_DISK
        else:
            context_file_type = CONTEXT_FILE_IN_MEMORY
        logger.debug(CHAPTER.format("context type: {}".format(context_file_type)))

    return fileobj


def make_build_context_from_dockerfile(dockerfile):
    f = six.BytesIO()
    with tarfile.open(mode='w', fileobj=f) as t:
        if isinstance(dockerfile, six.StringIO) or isinstance(dockerfile, io.StringIO):
            dfinfo = tarfile.TarInfo('Dockerfile')
            dfinfo.size = len(dockerfile.getvalue())
            dockerfile.seek(0)
        elif isinstance(dockerfile, six.BytesIO) or isinstance(dockerfile, io.BytesIO):
            dfinfo = tarfile.TarInfo('Dockerfile')
            dfinfo.size = len(dockerfile.getvalue())
            dockerfile.seek(0)
        else:
            dfinfo = t.gettarinfo(fileobj=dockerfile, arcname='Dockerfile')
        t.addfile(dfinfo, dockerfile)
    f.seek(0)
    return f


def get_name_and_tag(name):
    name_parts = name.split(':')
    if len(name_parts) == 2:
        repo = name_parts[0]
        tag = name_parts[1]
    else:
        repo = name
        tag = "latest"

    return repo, tag


def volumes_to_list(dict, mode=""):
    if mode:
        mode = ":" + mode
    else:
        mode = ""

    volumes = []
    for key, value in six.iteritems(dict):
        volumes.append("{}:{}{}".format(key, value, mode))
    return volumes


def volumes_to_bind_dict(dict, mode=""):
    volumes = {}
    for key, value in six.iteritems(dict):
        volumes[key] = {"bind": value,
                        "mode": mode
                        }
    return volumes


def volumes_to_dict(volumes):
    volumes = get_list_from_tuple_or_string(volumes)
    result = {}

    for v in volumes:
        v_split = v.split(':')
        result[v_split[0]] = v_split[1]

    return result


def get_list_from_tuple_or_string(value):
    if not value:
        return []
    if isinstance(value, six.string_types):
        return [value]
    else:
        return list(value)


def substitute_variables(text, variables):
    regex = "{([^}]*:-[^}]*)}"
    matches = re.finditer(regex, text)
    for m in matches:
        key, val = m.group(1).split(":-")
        variables.setdefault(key, val)

    regex_subst = "\$({[^}]*):-[^}]*}"
    text = re.sub(regex_subst, "$\g<1>}", text, 0)

    d = collections.defaultdict(lambda: "")
    d.update(variables)
    t = string.Template(text)
    return t.substitute(d)
