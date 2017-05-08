import pytest
import biobox.util as util

from biobox.exception import UnsupportedDockerVersionException

@pytest.mark.unsupported
def test_client_with_unsupported_docker_version():
    with pytest.raises(UnsupportedDockerVersionException) as excp:
        client = util.client()


def test_client_with_supported_docker_version():
    try:
        util.client()
    except UnsupportedDockerVersionException:
        pytest.fail("A supported Docker version should not raise an exception.")


def test_supported_docker_version():
    supported_versions = ['1.10.0', '1.11.0', '1.12.0', '1.13.0', '17.03.0', '17.04.0-ce']
    for v in supported_versions:
        assert util.is_supported_docker_version(v)
