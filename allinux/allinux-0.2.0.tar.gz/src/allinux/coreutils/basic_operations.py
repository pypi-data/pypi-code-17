#
# Basic operations
#

def cp(src, dst, *, recursive=False, follow_symlinks=True):
    """
    Mimic 'cp' command.
    
    recursive is True, mimic 'cp -r'.
    """
    if os.path.isdir(src):
        if recursive:
            shutil.copytree(src, dst, symlinks=follow_symlinks)
    else:
        shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
