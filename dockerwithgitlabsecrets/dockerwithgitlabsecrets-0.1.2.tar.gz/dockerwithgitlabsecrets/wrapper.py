import logging
import os
import subprocess
from tempfile import NamedTemporaryFile

from gitlabbuildvariables.manager import ProjectVariablesManager
from typing import List, Tuple, Optional, Dict

_DOCKER_ENV_FILE_SUFFIX = ".env"
_DOCKER_BINARY = "docker"
_SUPPORTED_DOCKER_ACTIONS = ["run"]

_LINE_BREAK = "\n"
SAFE_LINE_BREAK = "\\n"

_ENCODING = "utf-8"

StdOutType = str
StdErrType = str
ReturnCodeType = int
ProgramOutputType = Tuple[ReturnCodeType, StdOutType, StdErrType]

_logger = logging.getLogger(__name__)


def get_supported_action_index(docker_arguments: List[str]) -> Optional[int]:
    """
    TODO
    :param docker_arguments: 
    :return: 
    """
    if len(docker_arguments) == 0:
        return None

    docker_action_index = 0
    while docker_arguments[docker_action_index] not in _SUPPORTED_DOCKER_ACTIONS:
        docker_action_index += 1
        if docker_action_index == len(docker_arguments):
            return None
    return docker_action_index


def warn_if_new_lines_in_variables(variables: Dict[str, str]):
    """
    TODO
    :param variables: 
    :return: 
    """
    for key, value in variables.items():
        if _LINE_BREAK in value:
            _logger.warning(f"New line characters in variable with key \"{key}\" have been escaped to \\\\n")


def run_wrapped(docker_arguments: List[str], project_variables_manager: ProjectVariablesManager,
                env_file_location: str=None) -> ProgramOutputType:
    """
    TODO
    :param docker_arguments: 
    :param project_variables_manager: 
    :param env_file_location: 
    :return: 
    """
    docker_action_index = get_supported_action_index(docker_arguments)
    docker_call = [_DOCKER_BINARY]

    if docker_action_index is None:
        assert env_file_location is None
        docker_call += docker_arguments
        process = subprocess.Popen(docker_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
    else:
        with NamedTemporaryFile(suffix=_DOCKER_ENV_FILE_SUFFIX, mode="w") as env_file:
            if env_file_location is not None:
                with open(env_file_location, "r") as other_env_file:
                    env_file.write(other_env_file.read())

            variables = project_variables_manager.get()
            warn_if_new_lines_in_variables(variables)
            env_variables = os.linesep.join([f"{key}={value.replace(_LINE_BREAK, SAFE_LINE_BREAK)}"
                                             for key, value in variables.items()])
            env_file.write(env_variables)
            env_file.flush()

            from dockerwithgitlabsecrets.entrypoint import ENV_FILE_PARAMETER
            docker_call += docker_arguments[0:docker_action_index+1] + [f"--{ENV_FILE_PARAMETER}", env_file.name] \
                           + docker_arguments[docker_action_index+1:]
            process = subprocess.Popen(docker_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

    return process.returncode, stdout.decode(_ENCODING), stderr.decode(_ENCODING)
