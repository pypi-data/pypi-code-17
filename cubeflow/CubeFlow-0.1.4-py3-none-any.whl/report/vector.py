from typing import Iterable, Tuple, Callable
from math import log10, ceil
import matplotlib.pyplot as plt
from cubeflow.report import Report
from cubeflow.cube import T, CubeGrid


class VectorReport(Report[T]):

    def __init__(
            self,
            fileprefix: str,
            vectorise: Callable[[Tuple[Iterable[float], T]], Tuple[float, float, float, float]],
            title: str='Untitled',
            runs: int=None
    ) -> None:
        super().__init__(fileprefix)
        self._vectorise = vectorise
        self._title = title
        self._fills = ceil(log10(runs)) if runs else 0

    def __call__(self, grid: CubeGrid[T], t: float) -> None:
        x, y, u, v = zip(*[self._vectorise(coord) for coord in grid.coordinate_system])
        plt.figure()
        fig = plt.gcf()
        fig.set_size_inches(11, 8)
        quiver = plt.quiver(x, y, u, v, units='width')
        quiver_key = plt.quiverkey(
            quiver,
            0.9, 0.9, 2,
            self._title.format(t),
            labelpos='S',
            coordinates='figure'
        )
        index = str(self._index).zfill(self._fills)
        plt.savefig("{0}{1}.png".format(self._prefix, index), dpi=100)
        plt.close()
        self._index += 1
