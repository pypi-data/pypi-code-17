"""Test the command line interface.

Also take a look at test_client_with_server.py as it uses the command line interface.


TODO:
- What happens if unreachable?
- delete all resources
  - all of client
  - just those from the urls
  - from those urls which are unreachable  # TODO: implement in other tests, here: test parameter passing
- add several urls
- add a url list
- add both
- look at the resources on the server
- authentication
  - success
  - failure

Return codes:
- 0 everyting crawled or no urls given
- 1 crawling was interrupted by server  # TODO
- 2 could not reach all urls            # TODO
- 3 basic authentication failed
- 4 api token authentication failed
- 5 no authentication failed
- 6 can not reach the server
- 7 you can not use two authentication mechanisms
- 8 basic authentication needs a username and a password divided by :

"""
import schul_cloud_url_crawler.resource_client as resource_client
from schul_cloud_url_crawler.cli import main
import schul_cloud_resources_api_v1.auth as auth
from unittest.mock import Mock, call
from pytest import mark, raises, fixture
import click


@fixture
def raisesError(monkeypatch):
    """Return a function that can test for an error code and a description."""
    mock = Mock()
    monkeypatch.setattr(click, "echo", mock)
    def assertRaisesSystemExit(exit_code, description):
        text = "Error {}: {}".format(exit_code, description)
        def wrap(function):
            with raises(SystemExit) as error:
                function()
            assert error.value.code == exit_code
            mock.assert_called_with(text)
        return wrap
    return assertRaisesSystemExit


class TestAuthentication:
    """Test that the api authenticates."""

    @fixture
    def mock_auth(self, monkeypatch):
        """Return a mock which is used for authentication."""
        mock_auth = Mock()
        monkeypatch.setattr(auth, "basic", mock_auth.basic)
        monkeypatch.setattr(auth, "none", mock_auth.none)
        monkeypatch.setattr(auth, "api_key", mock_auth.api_key)
        return mock_auth

    def test_no_authentication_is_default(self, mock_auth, resources_server):
        """Test that a call to auth.none exits."""
        main(args=[resources_server.url], standalone_mode=False)
        mock_auth.none.assert_called_once_with()

    @mark.parametrize("username,password", [
            ["valid1@schul-cloud.org", "123abc"],
            ["valid2@schul-cloud.org", "supersecure"]
        ])
    def test_basic_authentication_uses_auth_method(
            self, mock_auth, username, password, resources_server):
        """Test that basic authentication provides the username and password."""
        main(args=["--basic={}:{}".format(username, password), resources_server.url], standalone_mode=False)
        mock_auth.basic.assert_called_once_with(username, password)

    @mark.parametrize("key", ["abcdefghijklmn"])
    def test_apikey_authentication_uses_auth_method(self, key, mock_auth, resources_server):
        """Test that the api key authentication is passed through to the auth module."""
        main(args=["--apikey={}".format(key), resources_server.url], standalone_mode=False)
        mock_auth.api_key.assert_called_once_with(key)

    @mark.parametrize("params", [
            ["--apikey=asflajkd", "--basic=asd:aasd"],
            ["--apikey=asflajkd", "--basic="],
            ["--apikey=", "--basic=asd:aasd"],
        ])
    def test_can_not_use_apikey_and_basic_authentication_at_the_same_time(
            self, raisesError, params, resources_server):
        """When two authentication mechanisms are used, the return code is"""
        @raisesError(7, "You can only provide one authentication mechanism with --basic and --apikey.")
        def main_error():
            main(args=params + [resources_server.url])

    @mark.parametrize("invalid_basic", ["--basic=", "--basic=asdasd"])
    def test_basic_authentication_needs_a_password(
            self, invalid_basic, raisesError, resources_server):
        @raisesError(8, "Basic authentication requires a username and a password divided by \":\". Example: --basic=user:password")
        def main_error():
            main(args=[invalid_basic, resources_server.url])

    @mark.parametrize("code,params,message", [
            (3, ["--basic=gdjfsd:jshfdkhshd"], "The resources server could be reached but basic authentication failed."),
            (4, ["--apikey=gdjfsdjshfdkhshd"], "The resources server could be reached but API-key authentication failed."),
            (5, [], "The resources server could be reached but it requires authentication with --basic or --apikey."),
        ])
    def test_authentication_failure(self, url401, code, params, message, raisesError):
        """Test the error codes for authentication."""
        @raisesError(code, message)
        def main_error():
            main(args=params + [url401])
    

def test_can_not_reach_the_server(raisesError):
    """Test what happens if the api could not be reached."""
    @raisesError(6, "The resource server could not be reached.")
    def main_error():
        main(args=["https://localhost:80/"])




class TestOptions:
    """Test the options --delete-all, --delete-not-updated and --id."""

    @fixture
    def mock_client(self, monkeypatch):
        """Return a mock which is used for authentication."""
        mock_client = Mock()
        monkeypatch.setattr(resource_client, "ResourceClient", mock_client)
        def assert_main_calls(args, expected_calls):
            """Make sure the calls to the client are expected."""
            main(args=args, standalone_mode=False)
            calls = mock_client().mock_calls
            assert calls == expected_calls
        mock_client.assert_main_calls = assert_main_calls
        return mock_client

    @mark.parametrize("_id,args", [
            ("url-crawler", []),
            ("asd", ["--id=asd"]),
            ("url-crawler-2", ["--id=url-crawler-2"]),
        ])
    def test_the__id(self, mock_client, _id, args):
        """Make sure that the default id is url-crawler."""
        main(args=["asdasda"] + args, standalone_mode=False)
        assert mock_client.call_count == 1
        arguments = mock_client.mock_calls[0][1]
        assert arguments[1] == _id

    def test_only_update_is_default(self, mock_client):
        """By default only the update function is called."""
        mock_client.assert_main_calls(["server-url"], [call.update([])])

    def test_delete_all(self, mock_client):
        """--delete-all deletes all resources before the crawling."""
        mock_client.assert_main_calls(["--delete-all", "server-url"], [call.delete_resources(), call.update([])])

    @mark.parametrize("urls", [["asd", "a"], [], ["asda", "wre", "rwfe"]])
    def test_delete_not_in_urls(self, mock_client, urls):
        """--delete-not-mentioned deletes these resources before crawling."""
        mock_client.assert_main_calls(
           ["--delete-not-mentioned", "server-url"] + urls,
           [call.delete_resources_not_from(urls), call.update(urls)])





