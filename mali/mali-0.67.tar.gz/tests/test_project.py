# coding=utf-8
import fudge
import httpretty
from click.testing import CliRunner
from fudge.inspector import arg

from mali_commands.projects import create_project
from tests.base import BaseTest


class TestProject(BaseTest):
    @httpretty.activate
    @fudge.patch('mali_commands.commons.handle_api')
    def test_create_project_no_org(self, handle_api):
        project_display_name = 'display_' + self.some_random_shit()

        handle_api.expects_call().with_matching_args(
            arg.any(), arg.any(),
            'projects',
            {
                'display_name': project_display_name
            },
            host='https://missinglink.ai',
            clientId='nbkyPAMoxj5tNzpP07vyrrsVZnhKYhMj',
            apiHost='https://missinglinkai.appspot.com',
            auth0='missinglink',
            outputFormat='tables'
        ).returns({})

        runner = CliRunner()
        result = runner.invoke(create_project, ['--displayName', project_display_name], catch_exceptions=False)
        self.assertEquals(result.exit_code, 0)

    @httpretty.activate
    @fudge.patch('mali_commands.commons.handle_api')
    def test_create_project_with_org(self, handle_api):
        org = 'org_' + self.some_random_shit()
        project_display_name = 'display_' + self.some_random_shit()

        handle_api.expects_call().with_matching_args(
            arg.any(), arg.any(),
            'projects',
            {
                'display_name': project_display_name,
                'org': org,
            },
            host='https://missinglink.ai',
            clientId='nbkyPAMoxj5tNzpP07vyrrsVZnhKYhMj',
            apiHost='https://missinglinkai.appspot.com',
            auth0='missinglink',
            outputFormat='tables'
        ).returns({})

        runner = CliRunner()
        result = runner.invoke(create_project, ['--displayName', project_display_name, '--org', org], catch_exceptions=False)
        self.assertEquals(result.exit_code, 0)
