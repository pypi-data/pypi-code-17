from typing import Generic, Optional, Tuple, Callable
from logging import getLogger, Logger
from cubeflow.cube import T, CubeGrid


class Report(Generic[T]):

    def __init__(self, prefix: str) -> None:
        self._prefix = prefix
        self._index = 0

    def __call__(self, grid: CubeGrid[T], t: float) -> None:
        pass


class Monitor(Generic[T]):
    ViolationCheck = Callable[[CubeGrid[T]], Optional[Tuple[int, str]]]

    def __init__(self, suffix: str, func: ViolationCheck, logger: Optional[Logger]) -> None:
        self._func = func
        self._logger = (logger if logger else getLogger('default')).getChild(suffix)

    def __call__(self, grid: CubeGrid[T]) -> None:
        result = self._func(grid)
        if result:
            self._logger.log(result[0], result[1])

