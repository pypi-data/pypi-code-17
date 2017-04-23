import pytest

from boogie.manager import QuerySetManager
from boogie.tests.testapp.models import ModelWithQsManager as Model


def test_model_manager_basic_interface():
    assert isinstance(Model.objects, QuerySetManager)
    assert Model.objects.name == 'objects'
    assert Model.objects.model is Model


def test_model_manager_basic_queries(db):
    assert len(Model.objects) == 0


class TestFilledDb:
    """
    Tests on a database filled with 3 objects.
    """

    @pytest.fixture
    def objs(self, db):
        obj1 = Model.objects.create(name='obj1', pk=1)
        obj2 = Model.objects.create(name='obj2', pk=2)
        return [obj1, obj2]

    def test_api_values_list(self, objs):
        names = Model.objects.values_list('name', flat=True)
        assert names.model is Model
        assert list(names) == ['obj1', 'obj2']

    def test_manager_as_sequence(self, objs):
        assert Model.objects.count() == 2
        assert Model.objects.all().count() == 2
        assert len(Model.objects) == 2
        assert list(Model.objects) == objs

    def test_indexing(self, objs):
        obj1, obj2 = objs
        assert Model.objects[obj1.pk] == obj1
        assert Model.objects[:] == [obj1, obj2]
        assert Model.objects[obj1.pk, 'name'] == 'obj1'

    def test_multi_col_indexing(self, objs):
        obj1, obj2 = objs
        res = Model.objects[obj1.pk, ['name']]
        assert res == ['obj1']
        assert res.name == 'obj1'
