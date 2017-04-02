import testincessantly

def test_exclude_paths_matching_patterns():
  f = testincessantly.exclusion.exclude_paths_matching_patterns
  assert f({'a', 'b'}, {'a'}) == {'b'}
  assert f({'a', 'b'}, {}) == {'a', 'b'}
  assert f({'a', 'b'}, {'*'}) == set()
  assert f({'a/b', 'c/d'}, {'c'}) == {'a/b'}
  assert f({'a/b', 'c/d'}, {'d'}) == {'a/b'}

def test_parse_pattern_file():
  f = testincessantly.exclusion.parse_pattern_file
  assert f(['', '', '# comment', 'a/*\n']) == {'a/*'}
  assert f(['', '', '# comment', 'a/\n']) == {'a'}
