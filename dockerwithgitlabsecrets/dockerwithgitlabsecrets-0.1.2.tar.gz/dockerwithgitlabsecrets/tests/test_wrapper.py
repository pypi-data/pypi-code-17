import unittest

from gitlab import Gitlab
from gitlabbuildvariables.common import GitLabConfig
from gitlabbuildvariables.manager import ProjectVariablesManager
from useintest.models import DockerisedServiceWithUsers
from useintest.predefined.gitlab import GitLab8_16_6_ce_0ServiceController
from useintest.services.controllers import DockerisedServiceController

from dockerwithgitlabsecrets.entrypoint import CONFIG_PARAMETER
from dockerwithgitlabsecrets.tests._common import EXAMPLE_PROJECT, EXAMPLE_VALUE, EXAMPLE_PARAMETER
from dockerwithgitlabsecrets.wrapper import run_wrapped, SAFE_LINE_BREAK

_GITLAB_PORT = 80
_PROJECT_VARIABLES = {
    "EXAMPLE": "value",
    "HELLO": "hello\nworld"
}


class TestWrapper(unittest.TestCase):
    """
    Tests for `run_wrapped`.
    """
    _gitlab_service: DockerisedServiceWithUsers
    _gitlab_controller: DockerisedServiceController
    project_variables_manager: ProjectVariablesManager
    project_name: str

    @classmethod
    def setUpClass(cls):
        cls._gitlab_controller = GitLab8_16_6_ce_0ServiceController()
        cls._gitlab_service = cls._gitlab_controller.start_service()
        gitlab_location = f"http://{cls._gitlab_service.host}:{cls._gitlab_service.ports[_GITLAB_PORT]}"

        gitlab = Gitlab(url=gitlab_location, email=cls._gitlab_service.root_user.username,
                        password=cls._gitlab_service.root_user.password)
        gitlab.auth()

        cls._gitlab_token = gitlab.private_token
        cls.project_name = f"{cls._gitlab_service.root_user.username}/{EXAMPLE_PROJECT}"
        gitlab.projects.create({"name": EXAMPLE_PROJECT})

        cls.project_variables_manager = ProjectVariablesManager(
            GitLabConfig(gitlab_location, cls._gitlab_token), cls.project_name)
        cls.project_variables_manager.set(_PROJECT_VARIABLES)

    @classmethod
    def tearDownClass(cls):
        cls._gitlab_controller.stop_service(cls._gitlab_service)

    def setUp(self):
        self.project_variables_manager = TestWrapper.project_variables_manager
        self.project_name = TestWrapper.project_name

    def test_help_with_docker_command(self):
        return_code, stdout, stderr = run_wrapped(["ps", "--help"], self.project_variables_manager)
        self.assertEquals(0, return_code)
        self.assertIn("Usage:\tdocker ps", stdout.strip())

    def test_with_non_supported_action(self):
        return_code, stdout, stderr = run_wrapped(["version"], self.project_variables_manager)
        self.assertEquals(0, return_code)
        self.assertIn("Version", stdout.strip())

    def test_has_standard_variable(self):
        return_code, stdout, stderr = run_wrapped(
            ["run", "-e", f"{EXAMPLE_PARAMETER}={EXAMPLE_VALUE}", "--rm", "alpine", "printenv", EXAMPLE_PARAMETER],
            self.project_variables_manager)
        self.assertEquals(0, return_code)
        self.assertEquals(EXAMPLE_VALUE, stdout.strip())

    def test_run_has_secret_variable(self):
        key, value = list(_PROJECT_VARIABLES.items())[0]
        return_code, stdout, stderr = run_wrapped(["--debug", "run", "--rm", "alpine", "printenv", key],
                                                  self.project_variables_manager)
        self.assertEquals(0, return_code)
        self.assertEquals(value, stdout.strip())

    def test_run_has_multiline_secret_variable(self):
        key, value = list(_PROJECT_VARIABLES.items())[1]
        return_code, stdout, stderr = run_wrapped(["run", "--rm", "alpine", "printenv", key],
                                                  self.project_variables_manager)
        self.assertEquals(0, return_code)
        self.assertEquals(value.replace("\n", SAFE_LINE_BREAK), stdout.strip())

    def test_run_cli_variable_has_higher_precedence(self):
        other_value = "other-value"
        key, value = list(_PROJECT_VARIABLES.items())[0]
        return_code, stdout, stderr = run_wrapped(["run", "-e", f"{key}={other_value}", "--rm", "alpine", "printenv",
                                                   key], self.project_variables_manager)
        self.assertEquals(0, return_code)
        self.assertEquals(other_value, stdout.strip())

    # TODO: Test execute
    # TODO: Test with --env-file


# TODO: Tests for run
    # def test_help(self):
    #     return_code, stdout, stderr = run_wrapped(["--help"], self.project_variables_manager)
    #     self.assertEquals(0, return_code)
    #     self.assertIn(CONFIG_PARAMETER, stdout.strip())




if __name__ == "__main__":
    unittest.main()
