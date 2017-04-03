import os.path
import fnmatch

def parse_pattern_file(file):
  stripped_lines = (line.strip().strip('/') for line in file)
  return set(line for line in stripped_lines if line and not line.startswith('#'))

def iter_segments(path):
  path = os.path.normpath(path)
  while path not in ['', '/']:
    path, basename = os.path.split(path)
    if basename: yield basename

def exclude_paths_matching_patterns(paths, patterns):
  paths = set(paths)
  excluded_paths = set(
    path
    for path in paths
    for segment in iter_segments(path)
    for pattern in patterns
    if fnmatch.fnmatch(segment, pattern))
  return paths - excluded_paths
