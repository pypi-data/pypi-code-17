from abc import abstractproperty, abstractmethod
from typing import Optional

from peek_plugin_base.PeekPlatformCommonHookABC import PeekPlatformCommonHookABC
from peek_plugin_base.PeekPlatformFrontendHookABC import PeekPlatformFrontendHookABC


class PeekServerPlatformHookABC(PeekPlatformCommonHookABC, PeekPlatformFrontendHookABC):
    @abstractproperty
    def dbConnectString(self) -> str:
        """ DB Connect String

        :return: The SQLAlchemy database engine connection string/url.

        """
