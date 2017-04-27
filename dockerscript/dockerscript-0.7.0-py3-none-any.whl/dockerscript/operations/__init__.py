"""
Dockerscript operators
"""

from .base_operation import Operation
from .base_image import base_image, BaseImageOperation
from .command import command, CommandOperation
from .copy import copy, CopyOperation
from .environment import environment, EnvironmentOperation
from .expose import expose, ExposeOperation
from .healthcheck import healthcheck, HealthcheckOperation
from .label import label, LabelOperation
from .run import run, RunOperation
from .shell import shell, ShellOperation
from .workdir import workdir, WorkdirOperation
