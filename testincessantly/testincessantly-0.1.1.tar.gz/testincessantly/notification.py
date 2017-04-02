import os.path
import fnmatch
import logging
import inotify.adapters

def iter_modified_file_paths(target_directory):
  i = inotify.adapters.InotifyTree(target_directory.encode())

  def _helper():
    for event in i.event_gen():
      if event is None: continue
      _, flags, directory_name, file_name = event
      path = os.path.normpath(os.path.join(directory_name, file_name))
      if set(flags) & set(['IN_CREATE', 'IN_MODIFY', 'IN_DELETE']):
        logging.debug('{!r} on file {!r}'.format(flags, path))
        yield path.decode()

  return _helper()
