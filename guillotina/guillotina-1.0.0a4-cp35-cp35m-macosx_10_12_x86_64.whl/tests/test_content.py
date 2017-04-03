from guillotina import configure
from guillotina.component import getUtility
from guillotina.content import create_content
from guillotina.content import create_content_in_container
from guillotina.content import Folder
from guillotina.content import load_cached_schema
from guillotina.exceptions import NoPermissionToAdd
from guillotina.exceptions import NotAllowedContentType
from guillotina.interfaces import IApplication
from guillotina.interfaces.types import IConstrainTypes
from guillotina.tests import utils

import pytest


@pytest.mark.usefixtures("dummy_request")
class TestContent:
    async def test_not_allowed_to_create_content(self, dummy_request):
        self.request = dummy_request

        container = await create_content(
            'Container',
            id='guillotina',
            title='Guillotina')
        container.__name__ = 'guillotina'

        with pytest.raises(NoPermissionToAdd):
            # not logged in, can't create
            await create_content_in_container(container, 'Item', id_='foobar')

    async def test_allowed_to_create_content(self, dummy_request):
        self.request = dummy_request
        utils.login(self.request)

        container = await create_content(
            'Container',
            id='guillotina',
            title='Guillotina')
        container.__name__ = 'guillotina'
        utils._p_register(container)

        await create_content_in_container(container, 'Item', id_='foobar')

    async def test_allowed_types(self, dummy_request):
        self.request = dummy_request
        utils.login(self.request)

        container = await create_content(
            'Container',
            id='guillotina',
            title='Guillotina')
        container.__name__ = 'guillotina'
        utils._p_register(container)

        import guillotina.tests
        configure.register_configuration(Folder, dict(
            type_name="TestType",
            allowed_types=['Item'],
            module=guillotina.tests  # for registration initialization
        ), 'contenttype')
        root = getUtility(IApplication, name='root')

        configure.load_configuration(
            root.app.config, 'guillotina.tests', 'contenttype')
        root.app.config.execute_actions()
        load_cached_schema()

        obj = await create_content_in_container(container, 'TestType', 'foobar')

        constrains = IConstrainTypes(obj, None)
        assert constrains.get_allowed_types() == ['Item']
        assert constrains.is_type_allowed('Item')

        with pytest.raises(NotAllowedContentType):
            await create_content_in_container(obj, 'TestType', 'foobar')
        await create_content_in_container(obj, 'Item', 'foobar')
