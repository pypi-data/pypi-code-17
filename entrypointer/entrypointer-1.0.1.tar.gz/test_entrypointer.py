import collections

import pkg_resources
import pytest

import entrypointer


class TestAttrGroup(object):
    def test_init(self):
        result = entrypointer.AttrGroup('prefix.')

        assert result._prefix == 'prefix.'
        assert result._attr_cache == {}

    def test_getattr_cached(self, mocker):
        mock_EntrypointDict = mocker.patch.object(
            entrypointer, 'EntrypointDict'
        )
        obj = entrypointer.AttrGroup('prefix.')
        obj._attr_cache['spam'] = 'cached'

        assert obj.spam == 'cached'
        assert obj._attr_cache == {'spam': 'cached'}
        assert not mock_EntrypointDict.called

    def test_getattr_uncached(self, mocker):
        mock_EntrypointDict = mocker.patch.object(
            entrypointer, 'EntrypointDict'
        )
        obj = entrypointer.AttrGroup('prefix.')

        assert obj.spam == mock_EntrypointDict.return_value
        assert obj._attr_cache == {'spam': mock_EntrypointDict.return_value}
        mock_EntrypointDict.assert_called_once_with('prefix.spam')

    def test_getattr_internal(self, mocker):
        mock_EntrypointDict = mocker.patch.object(
            entrypointer, 'EntrypointDict'
        )
        obj = entrypointer.AttrGroup('prefix.')

        with pytest.raises(AttributeError):
            obj._spam
        assert obj._attr_cache == {}
        assert not mock_EntrypointDict.called

    def test_getattr_nested(self, mocker):
        mock_EntrypointDict = mocker.patch.object(
            entrypointer, 'EntrypointDict'
        )
        ep = mock_EntrypointDict.return_value
        obj = entrypointer.AttrGroup('prefix.')

        result = getattr(obj, 'spam.spam.spam.spam')

        assert result == ep.spam.spam.spam
        assert obj._attr_cache == {'spam': ep}
        mock_EntrypointDict.assert_called_once_with('prefix.spam')


class TestEntrypointList(object):
    def test_init(self):
        result = entrypointer.EntrypointList('group', 'name')

        assert result._group == 'group'
        assert result._name == 'name'
        assert result._eps == []
        assert result._found is False
        assert result._explored is False
        assert result._entries == set()

    def test_str(self, mocker):
        mocker.patch.object(
            entrypointer.EntrypointList,
            '__iter__',
            return_value=iter(['ep1', 'ep2', 'ep3']),
        )
        obj = entrypointer.EntrypointList('group', 'name')

        result = str(obj)

        assert result == '[ep1, ep2, ep3]'

    def test_repr(self):
        obj = entrypointer.EntrypointList('group', 'name')

        result = repr(obj)

        assert result == (
            '<entrypointer.EntrypointList object at 0x%x>' % id(obj)
        )

    def test_len(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointList, '_find')
        obj = entrypointer.EntrypointList('group', 'name')
        obj._eps = ['ep1', 'ep2', 'ep3']

        result = len(obj)

        assert result == 3
        mock_find.assert_called_once_with()

    def test_getitem_badidx(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointList, '_find')
        obj = entrypointer.EntrypointList('group', 'name')
        obj._eps = ['ep1', 'ep2', 'ep3']

        with pytest.raises(TypeError):
            obj['bad']
        assert not mock_find.called

    def test_getitem_idx0(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointList, '_find')
        obj = entrypointer.EntrypointList('group', 'name')
        obj._eps = ['ep1', 'ep2', 'ep3']

        assert obj[0] == 'ep1'
        mock_find.assert_called_once_with(True)

    def test_getitem_idx1(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointList, '_find')
        obj = entrypointer.EntrypointList('group', 'name')
        obj._eps = ['ep1', 'ep2', 'ep3']

        assert obj[1] == 'ep2'
        mock_find.assert_called_once_with()

    def test_getitem_slice(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointList, '_find')
        obj = entrypointer.EntrypointList('group', 'name')
        obj._eps = ['ep1', 'ep2', 'ep3']

        assert obj[:] == ['ep1', 'ep2', 'ep3']
        mock_find.assert_called_once_with()

    def test_bool_empty(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointList, '_find')
        obj = entrypointer.EntrypointList('group', 'name')

        assert bool(obj) is False
        mock_find.assert_called_once_with(True)

    def test_bool_nonempty(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointList, '_find')
        obj = entrypointer.EntrypointList('group', 'name')
        obj._eps = ['ep1', 'ep2', 'ep3']

        assert bool(obj) is True
        mock_find.assert_called_once_with(True)

    def test_find_explored_one(self, mocker):
        mock_iter_entry_points = mocker.patch.object(
            entrypointer.pkg_resources,
            'iter_entry_points',
            return_value=[],
        )
        obj = entrypointer.EntrypointList('group', 'name')
        obj._explored = True

        obj._find(True)

        assert not mock_iter_entry_points.called
        assert obj._eps == []
        assert obj._found is False
        assert obj._explored is True
        assert obj._entries == set()

    def test_find_explored_all(self, mocker):
        mock_iter_entry_points = mocker.patch.object(
            entrypointer.pkg_resources,
            'iter_entry_points',
            return_value=[],
        )
        obj = entrypointer.EntrypointList('group', 'name')
        obj._explored = True

        obj._find()

        assert not mock_iter_entry_points.called
        assert obj._eps == []
        assert obj._found is False
        assert obj._explored is True
        assert obj._entries == set()

    def test_find_found_one(self, mocker):
        mock_iter_entry_points = mocker.patch.object(
            entrypointer.pkg_resources,
            'iter_entry_points',
            return_value=[],
        )
        obj = entrypointer.EntrypointList('group', 'name')
        obj._found = True

        obj._find(True)

        assert not mock_iter_entry_points.called
        assert obj._eps == []
        assert obj._found is True
        assert obj._explored is False
        assert obj._entries == set()

    def test_find_one(self, mocker):
        eps = [
            mocker.Mock(**{'load.side_effect': ImportError()}),
            mocker.Mock(**{'load.side_effect': AttributeError()}),
            mocker.Mock(**{'load.side_effect': pkg_resources.UnknownExtra()}),
            mocker.Mock(**{'load.return_value': 'obj1'}),
            mocker.Mock(**{'load.return_value': 'obj2'}),
        ]
        mock_iter_entry_points = mocker.patch.object(
            entrypointer.pkg_resources,
            'iter_entry_points',
            return_value=eps,
        )
        obj = entrypointer.EntrypointList('group', 'name')

        obj._find(True)

        mock_iter_entry_points.assert_called_once_with('group', 'name')
        assert obj._eps == ['obj1']
        assert obj._found is True
        assert obj._explored is False
        assert obj._entries == set([id(ep) for ep in eps[:4]])
        for i, ep in enumerate(eps):
            if i == len(eps) - 1:
                assert not ep.load.called
            else:
                ep.load.assert_called_once_with()

    def test_find_all(self, mocker):
        eps = [
            mocker.Mock(**{'load.side_effect': ImportError()}),
            mocker.Mock(**{'load.side_effect': AttributeError()}),
            mocker.Mock(**{'load.side_effect': pkg_resources.UnknownExtra()}),
            mocker.Mock(**{'load.return_value': 'obj1'}),
            mocker.Mock(**{'load.return_value': 'obj2'}),
            mocker.Mock(**{'load.return_value': 'skipped'}),
        ]
        mock_iter_entry_points = mocker.patch.object(
            entrypointer.pkg_resources,
            'iter_entry_points',
            return_value=eps,
        )
        obj = entrypointer.EntrypointList('group', 'name')
        obj._entries.add(id(eps[-1]))

        obj._find()

        mock_iter_entry_points.assert_called_once_with('group', 'name')
        assert obj._eps == ['obj1', 'obj2']
        assert obj._found is True
        assert obj._explored is True
        assert obj._entries == set([id(ep) for ep in eps])
        for i, ep in enumerate(eps):
            if i == len(eps) - 1:
                assert not ep.load.called
            else:
                ep.load.assert_called_once_with()

    def test_group(self):
        obj = entrypointer.EntrypointList('group', 'name')

        assert obj.group == 'group'

    def test_name(self):
        obj = entrypointer.EntrypointList('group', 'name')

        assert obj.name == 'name'


class TestEntrypointDict(object):
    def test_init(self, mocker):
        mock_init = mocker.patch.object(
            entrypointer.AttrGroup, '__init__', return_value=None
        )

        result = entrypointer.EntrypointDict('group')

        assert result._group == 'group'
        assert result._entries == {}
        assert result._explored is False
        mock_init.assert_called_once_with('group.')

    def test_str(self):
        obj = entrypointer.EntrypointDict('group')
        obj._entries = collections.OrderedDict([
            ('ep1', 'obj1'),
            ('ep2', 'obj2'),
            ('ep3', 'obj3'),
        ])

        result = str(obj)

        assert result == '{%r: obj1, %r: obj2, %r: obj3}' % (
            'ep1', 'ep2', 'ep3'
        )

    def test_repr(self):
        obj = entrypointer.EntrypointDict('group')

        result = repr(obj)

        assert result == (
            '<entrypointer.EntrypointDict object at 0x%x>' % id(obj)
        )

    def test_getitem_badkey(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList'
        )
        obj = entrypointer.EntrypointDict('group')

        with pytest.raises(KeyError):
            obj[1234]
        assert obj._entries == {}
        assert not mock_EntrypointList.called

    def test_getitem_cached(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList'
        )
        obj = entrypointer.EntrypointDict('group')
        obj._entries['spam'] = ['cached']

        assert obj['spam'] == 'cached'
        assert obj._entries == {'spam': ['cached']}
        assert not mock_EntrypointList.called

    def test_getitem_empty(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList'
        )
        obj = entrypointer.EntrypointDict('group')
        obj._entries['spam'] = []

        with pytest.raises(KeyError):
            obj['spam']
        assert obj._entries == {'spam': []}
        assert not mock_EntrypointList.called

    def test_getitem_uncached(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList', return_value=['obj1', 'obj2']
        )
        obj = entrypointer.EntrypointDict('group')

        assert obj['spam'] == 'obj1'
        assert obj._entries == {'spam': ['obj1', 'obj2']}
        mock_EntrypointList.assert_called_once_with('group', 'spam')

    def test_len(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointDict, '_find')
        obj = entrypointer.EntrypointDict('group')
        obj._entries = {
            'ep1': [],
            'ep2': ['obj1'],
            'ep3': ['obj2', 'obj3'],
            'ep4': [],
        }

        result = len(obj)

        assert result == 2
        mock_find.assert_called_once_with()

    def test_iter(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointDict, '_find')
        obj = entrypointer.EntrypointDict('group')
        obj._entries = collections.OrderedDict([
            ('ep1', []),
            ('ep2', ['obj1']),
            ('ep3', ['obj2', 'obj3']),
            ('ep4', []),
        ])

        result = list(iter(obj))

        assert result == ['ep2', 'ep3']
        mock_find.assert_called_once_with()

    def test_find_explored(self, mocker):
        mock_iter_entry_points = mocker.patch.object(
            entrypointer.pkg_resources,
            'iter_entry_points',
            return_value=[],
        )
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList'
        )
        obj = entrypointer.EntrypointDict('group')
        obj._explored = True

        obj._find()

        assert not mock_iter_entry_points.called
        assert not mock_EntrypointList.called
        assert obj._explored is True
        assert obj._entries == {}

    def test_find_unexplored(self, mocker):
        eps = [
            mocker.Mock(**{
                'epname': 'ep1',
                'load.side_effect': ImportError(),
            }),
            mocker.Mock(**{
                'epname': 'ep2',
                'load.side_effect': AttributeError(),
            }),
            mocker.Mock(**{
                'epname': 'ep1',
                'load.side_effect': pkg_resources.UnknownExtra(),
            }),
            mocker.Mock(**{
                'epname': 'ep3',
                'load.return_value': 'obj1',
            }),
            mocker.Mock(**{
                'epname': 'ep1',
                'load.return_value': 'obj2',
            }),
            mocker.Mock(**{
                'epname': 'ep2',
                'load.return_value': 'skipped',
            }),
        ]
        lists = {}
        for ep in eps:
            ep.name = ep.epname
            lst = lists.setdefault(ep.epname, mocker.Mock(
                _entries=set(),
                _eps=[],
                _found=False,
                _explored=False,
                _entries_expected=set(),
                _eps_expected=[],
            ))
            lst._entries_expected.add(id(ep))
            if not isinstance(ep.load.return_value, mocker.Mock):
                if ep.load.return_value == 'skipped':
                    lst._entries.add(id(ep))
                else:
                    lst._eps_expected.append(ep.load.return_value)
        mock_iter_entry_points = mocker.patch.object(
            entrypointer.pkg_resources,
            'iter_entry_points',
            return_value=eps,
        )
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList', side_effect=lambda x, y: lists[y]
        )
        obj = entrypointer.EntrypointDict('group')

        obj._find()

        mock_iter_entry_points.assert_called_once_with('group')
        mock_EntrypointList.assert_has_calls([
            mocker.call('group', name) for name in lists
        ], any_order=True)
        assert obj._explored is True
        assert obj._entries == lists
        for lst in obj._entries.values():
            assert lst._eps == lst._eps_expected
            assert lst._entries == lst._entries_expected
            assert lst._found is True
            assert lst._explored is True

    def test_items_all(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointDict, '_find')
        obj = entrypointer.EntrypointDict('group')
        obj._entries = collections.OrderedDict([
            ('ep1', []),
            ('ep2', ['obj1']),
            ('ep3', ['obj2', 'obj3']),
            ('ep4', []),
        ])

        result = list(obj.items_all())

        assert result == [('ep2', ['obj1']), ('ep3', ['obj2', 'obj3'])]
        mock_find.assert_called_once_with()

    def test_values_all(self, mocker):
        mock_find = mocker.patch.object(entrypointer.EntrypointDict, '_find')
        obj = entrypointer.EntrypointDict('group')
        obj._entries = collections.OrderedDict([
            ('ep1', []),
            ('ep2', ['obj1']),
            ('ep3', ['obj2', 'obj3']),
            ('ep4', []),
        ])

        result = list(obj.values_all())

        assert result == [['obj1'], ['obj2', 'obj3']]
        mock_find.assert_called_once_with()

    def test_get_all_badkey(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList'
        )
        obj = entrypointer.EntrypointDict('group')

        assert obj.get_all(1234) is None
        assert obj._entries == {}
        assert not mock_EntrypointList.called

    def test_get_all_badkey_default(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList'
        )
        obj = entrypointer.EntrypointDict('group')

        assert obj.get_all(1234, 'default') == 'default'
        assert obj._entries == {}
        assert not mock_EntrypointList.called

    def test_get_all_cached(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList'
        )
        obj = entrypointer.EntrypointDict('group')
        obj._entries['spam'] = ['cached']

        assert obj.get_all('spam') == ['cached']
        assert obj._entries == {'spam': ['cached']}
        assert not mock_EntrypointList.called

    def test_get_all_cached_default(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList'
        )
        obj = entrypointer.EntrypointDict('group')
        obj._entries['spam'] = ['cached']

        assert obj.get_all('spam', 'default') == ['cached']
        assert obj._entries == {'spam': ['cached']}
        assert not mock_EntrypointList.called

    def test_get_all_empty(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList'
        )
        obj = entrypointer.EntrypointDict('group')
        obj._entries['spam'] = []

        assert obj.get_all('spam') is None
        assert obj._entries == {'spam': []}
        assert not mock_EntrypointList.called

    def test_get_all_empty_default(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList'
        )
        obj = entrypointer.EntrypointDict('group')
        obj._entries['spam'] = []

        assert obj.get_all('spam', 'default') == 'default'
        assert obj._entries == {'spam': []}
        assert not mock_EntrypointList.called

    def test_get_all_uncached(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList', return_value=['obj1', 'obj2']
        )
        obj = entrypointer.EntrypointDict('group')

        assert obj.get_all('spam') == ['obj1', 'obj2']
        assert obj._entries == {'spam': ['obj1', 'obj2']}
        mock_EntrypointList.assert_called_once_with('group', 'spam')

    def test_get_all_uncached_default(self, mocker):
        mock_EntrypointList = mocker.patch.object(
            entrypointer, 'EntrypointList', return_value=['obj1', 'obj2']
        )
        obj = entrypointer.EntrypointDict('group')

        assert obj.get_all('spam', 'default') == ['obj1', 'obj2']
        assert obj._entries == {'spam': ['obj1', 'obj2']}
        mock_EntrypointList.assert_called_once_with('group', 'spam')

    def test_group(self):
        obj = entrypointer.EntrypointDict('group')

        assert obj.group == 'group'


class TestEps(object):
    def test_base(self):
        assert isinstance(entrypointer.eps, entrypointer.AttrGroup)
        assert entrypointer.eps._prefix == ''
