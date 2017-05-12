import os
import unittest
from tempfile import mkstemp

import yaml
from typing import Dict

from dockerwithgitlabsecrets.configuration import GITLAB_PROPERTY, GITLAB_URL_PROPERTY, GITLAB_TOKEN_PROPERTY, \
    GITLAB_NAMESPACE_PROPERTY, GITLAB_PROJECT_PROPERTY, parse_configuration, Configuration, GitLabConfiguration
from dockerwithgitlabsecrets.tests._common import EXAMPLE_URL, EXAMPLE_TOKEN, EXAMPLE_NAMESPACE, EXAMPLE_PROJECT


class TestParseConfiguration(unittest.TestCase):
    """
    Tests for `parse_configuration`.
    """
    def setUp(self):
        self._temp_file_handle, self._temp_file_location = mkstemp()

    def tearDown(self):
        os.remove(self._temp_file_location)

    def test_parse_minimal_configuration(self):
        self._json_to_temp_file({
            GITLAB_PROPERTY: {
                GITLAB_URL_PROPERTY: EXAMPLE_URL,
                GITLAB_TOKEN_PROPERTY: EXAMPLE_TOKEN
            }
        })
        expected = Configuration(GitLabConfiguration(url=EXAMPLE_URL, token=EXAMPLE_TOKEN))
        self.assertEquals(expected, parse_configuration(self._temp_file_location))

    def test_parse_full_configuration(self):
        self._json_to_temp_file({
            GITLAB_PROPERTY: {
                GITLAB_URL_PROPERTY: EXAMPLE_URL,
                GITLAB_TOKEN_PROPERTY: EXAMPLE_TOKEN,
                GITLAB_PROJECT_PROPERTY: EXAMPLE_PROJECT,
                GITLAB_NAMESPACE_PROPERTY: EXAMPLE_NAMESPACE
            }
        })
        expected = Configuration(GitLabConfiguration(
            url=EXAMPLE_URL, token=EXAMPLE_TOKEN, project=EXAMPLE_PROJECT, namespace=EXAMPLE_NAMESPACE))
        self.assertEquals(expected, parse_configuration(self._temp_file_location))

    def _json_to_temp_file(self, json: Dict):
        """
        Writes the equivalent YAML to the given JSON in the temp file.
        :param json: the JSON to convert to YAML
        """
        with open(self._temp_file_location, "w") as file:
            yaml.dump(json, file)


if __name__ == "__main__":
    unittest.main()
