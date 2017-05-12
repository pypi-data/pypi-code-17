import unittest

from dockerwithgitlabsecrets.entrypoint import CliConfiguration, parse_cli_arguments, CONFIG_PARAMETER, \
    PROJECT_PARAMETER, ENV_FILE_PARAMETER
from dockerwithgitlabsecrets.tests._common import EXAMPLE_PROJECT, EXAMPLE_LOCATION, EXAMPLE_LOCATION_2, \
    EXAMPLE_DOCKER_ARGS

_CONFIG_PARAMETER_FLAG = f"--{CONFIG_PARAMETER}"
_PROJECT_PARAMETER_FLAG = f"--{PROJECT_PARAMETER}"
_ENV_FILE_PARAMETER_FLAG = f"--{ENV_FILE_PARAMETER}"


class TestParseCliArguments(unittest.TestCase):
    """
    Tests for `parse_cli_arguments`.
    """
    def test_parse_only_config_location_argument(self):
        arguments = [_CONFIG_PARAMETER_FLAG, EXAMPLE_LOCATION]
        expected = CliConfiguration(config_location=EXAMPLE_LOCATION)
        self.assertEquals(expected, parse_cli_arguments(arguments))

    def test_parse_only_project_argument(self):
        arguments = [_PROJECT_PARAMETER_FLAG, EXAMPLE_PROJECT]
        expected = CliConfiguration(project=EXAMPLE_PROJECT)
        self.assertEquals(expected, parse_cli_arguments(arguments))

    def test_parse_program_arguments_with_docker_arguments(self):
        arguments = [_CONFIG_PARAMETER_FLAG, EXAMPLE_LOCATION, _PROJECT_PARAMETER_FLAG, EXAMPLE_PROJECT] \
                    + EXAMPLE_DOCKER_ARGS
        expected = CliConfiguration(project=EXAMPLE_PROJECT, config_location=EXAMPLE_LOCATION,
                                    docker_args=EXAMPLE_DOCKER_ARGS)
        self.assertEquals(expected, parse_cli_arguments(arguments))

    def test_parse_program_arguments_with_env_docker_argument(self):
        arguments = [_CONFIG_PARAMETER_FLAG, EXAMPLE_LOCATION, _PROJECT_PARAMETER_FLAG, EXAMPLE_PROJECT,
                     _ENV_FILE_PARAMETER_FLAG, EXAMPLE_LOCATION_2] + EXAMPLE_DOCKER_ARGS
        expected = CliConfiguration(project=EXAMPLE_PROJECT, config_location=EXAMPLE_LOCATION,
                                    env_file=EXAMPLE_LOCATION_2, docker_args=EXAMPLE_DOCKER_ARGS)
        configuration = parse_cli_arguments(arguments)
        self.assertEquals(expected, configuration)
        self.assertNotIn(ENV_FILE_PARAMETER, configuration.docker_args)


if __name__ == '__main__':
    unittest.main()
