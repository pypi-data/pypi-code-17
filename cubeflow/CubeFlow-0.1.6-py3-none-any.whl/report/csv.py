from typing import Sequence
from cubeflow.report import Report
from cubeflow.cube import T, CubeGrid


class CSVReport(Report[T]):
    """
    Provides a means for storing the course of the simulation as csv files, one
    file for each simulation step. You have to specify a converter if your data
    cells do not use MetaCell as metaclass.
    """

    def __init__(self, fileprefix: str, convert=lambda x: x.values()) -> None:
        super().__init__(fileprefix)
        self._converter = convert
        self._headline = None
        self.delta = (0.5, 0.5)

    def __call__(self, grid: CubeGrid[T], t: float) -> None:
        with open("{0}.csv.{1}".format(self._prefix, self._index), 'w') as out:
            if not self._headline:
                self._headline = list("xyzuvw"[0:grid.dimension])
                self._headline.append('t')
                self._headline.extend(grid[0].names())
            out.write(','.join(self._headline) + '\n')
            for (coord, cell) in grid.coordinate_system:
                cell_data = list(self.move(coord))
                cell_data.append(t)
                cell_data.extend(self._converter(cell))
                out.write(','.join(map(str, cell_data)))
                out.write('\n')
            self._index += 1

    def move(self, coord: Sequence[int]) -> Sequence[float]:
        return tuple((c+d for (c, d) in zip(coord, self.delta)))
