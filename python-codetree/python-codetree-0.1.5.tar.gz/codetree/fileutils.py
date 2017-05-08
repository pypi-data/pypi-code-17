import subprocess
import shutil
import os
import errno


class FileManipulationError(Exception):
    pass


def copy(source, dest):
    rsync(source, dest, delete=False)


def rsync(source, dest, delete=True, perms=True, links=True, times=False):
    short_args = ["-"]
    long_args = []
    if os.path.isdir(source):
        if not source.endswith("/"):
            # The contents of source are always copied into a folder
            # with the name of dest
            source = source + "/"
        short_args.append("r")
        if delete:
            long_args.append("--delete")
    elif not os.path.isfile(source):
        raise FileManipulationError("Only files and directories can be copied")

    if perms:
        short_args.append("p")
    if links:
        short_args.append("l")
    if times:
        short_args.append("t")

    cmd = ["rsync"]
    if short_args:
        cmd.append("".join(short_args))
    if long_args:
        cmd.extend(long_args)
    cmd.extend([source, dest])

    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        raise FileManipulationError(e.message)


def link(source, dest=None, symbolic=True, overwrite=True):
    if not dest:
        source_name = os.path.basename(source)
        current_dir = os.getcwd()
        dest = os.path.join(current_dir, source_name)
    elif not os.path.isabs(dest):
        # Ensure we always use an absolute path to prevent bug#1534612
        current_dir = os.getcwd()
        dest = os.path.join(current_dir, dest)
    if os.path.islink(dest):
        # This will trigger for a pre-existing symlink
        if overwrite:
            os.unlink(dest)
        else:
            raise FileManipulationError(
                "Destination already exists as symlink: {}".format(dest))
    elif os.path.exists(dest):
        # This won't trigger for a pre-existing symlink
        raise FileManipulationError("Destination already exists: {}".format(dest))

    if symbolic:
        mklink = os.symlink
    else:
        mklink = os.link

    try:
        mklink(source, dest)
    except OSError as e:
        raise FileManipulationError(e.message)


def mkdir(dirname, overwrite=False):
    if os.path.exists(dirname):
        if overwrite:
            shutil.rmtree(dirname)
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        else:
            raise FileManipulationError("Creation of directory failed: {}".format(dirname), e)
