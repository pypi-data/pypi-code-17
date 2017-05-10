# coding=utf-8
import fudge
import httpretty
from mali_commands.auth import init_auth
from .base import BaseTest
from click.testing import CliRunner


class TestAuth(BaseTest):
    @httpretty.activate
    @fudge.patch('mali_commands.commons.pixy_flow')
    @fudge.patch('mali_commands.config.Config.update_and_save')
    def test_init_auth(self, pixy_flow, update_and_save_config):
        access_token = 'access_token'
        refresh_token = 'refresh_token'
        id_token = 'id_token'

        pixy_flow.expects_call().returns((access_token, refresh_token, id_token)).times_called(1)
        update_and_save_config.expects_call().with_args(
            {
                'token': {
                    'access_token': access_token,
                    'id_token': id_token,
                    'refresh_token': refresh_token
                }
            }
        ).returns(None).times_called(1)

        runner = CliRunner()
        result = runner.invoke(init_auth, catch_exceptions=False)
        self.assertEquals(result.exit_code, 0)
