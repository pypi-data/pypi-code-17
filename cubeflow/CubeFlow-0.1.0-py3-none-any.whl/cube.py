from typing import List, Tuple, Iterable, Dict, TypeVar, Callable, Generic, Sequence, Any, Union
from json import load
from itertools import count, product
from operator import mul
from functools import reduce

T = TypeVar('T')

Neighbours = Dict[Iterable[int], T]


def _default_converter(type_: int, **data: Dict[str, float]) -> Dict[str, Union[int, float]]:
    return dict(type=type_, **data)


class CubeGrid(Generic[T]):
    @property
    def borders(self) -> List[int]:
        return list(self._border_indices)

    @property
    def cells(self) -> List[int]:
        return list(self._cell_indices)

    @property
    def grid(self) -> List[T]:
        return self._cells

    @property
    def coordinate_system(self) -> Iterable[Tuple[Iterable[float], T]]:
        return [
            (self._get_coordinates(index), self._cells[index])
            for index in range(len(self._cells))
        ]

    @property
    def layout(self) -> List[Iterable[int]]:
        return self._layout

    @property
    def dimension(self) -> int:
        return len(self._dim)

    @property
    def lengths(self) -> Sequence[float]:
        return self._lengths

    def __init__(self, *dimensions: Iterable[int]) -> None:
        self._dim = dimensions
        self._cells = []
        self._border_indices = []
        self._cell_indices = []
        self._offsets = [reduce(mul, dimensions[0:i], 1) for i in range(len(self._dim))]
        self._layout = self._create_layout()
        self._lengths = (1,) * len(self._dim)

    def load(self, buffer, converter=_default_converter) -> None:
        """
        :param buffer:
        :return:
        >>> grid = CubeGrid(3, 4)
        >>> grid.load(open('../sample.json', 'r'))
        >>> len(grid._cells)
        12
        >>> grid._cell_indices
        [5, 6]
        """
        specs = load(buffer)
        self._dim = specs['dimensions']
        self._offsets = [reduce(mul, self._dim[0:i], 1) for i in range(len(self._dim))]
        self._lengths = tuple(specs['deltas'].values())
        for (i, cell) in zip(count(), specs['cells']):
            self._cells.append(converter(cell['type'], **cell['data']))
            if cell['type']:
                self._border_indices.append(i)
            else:
                self._cell_indices.append(i)

        self._layout = self._create_layout()

    def neighbours(self, index: int) -> List[Tuple[int, int]]:
        """
        :param index:
        :return:
        >>> grid = CubeGrid(4, 3)
        >>> grid._cells = list(range(4*3))
        >>> grid.neighbours(5)
        {(0, 1): 9, (-1, 1): 8, (0, 0): 5, (-1, 0): 4, (-1, -1): 0, (0, -1): 1, (1, 0): 6, (1, -1): 2, (1, 1): 10}
        >>> grid.neighbours(0)
        {(0, 1): 4, (-1, 1): None, (0, 0): 0, (-1, 0): None, (-1, -1): None, (0, -1): None, (1, 0): 1, (1, -1): None, (1, 1): 5}
        """
        center = self._get_coordinates(index)
        return dict([
            (coord, self[self._get_index([c+x for (c, x) in zip(coord, center)])])
            for coord in product((0, 1, -1), repeat=len(self._offsets))
        ])

    def apply_function(self, func: Callable[[Neighbours], T], inner_only: bool=True) -> None:
        for index in self._cell_indices if inner_only else range(len(self._cells)):
            updated = func(self.neighbours(index))
            if not updated:
                raise ValueError("apply_function: func {0} returned None value".format(func))
            self[index] = updated

    def apply_function_border(self, func: Callable[[Neighbours], T]) -> None:
        for index in self._border_indices:
            self[index] = func(self.neighbours(index))

    def handle_borders(self, func: Callable[[Neighbours], T]) -> None:
        for index in self._border_indices:
            self[index] = func(self.neighbours(index))

    def simulate_while(self, simulator, border, predicate, protocol=None) -> int:
        runs = 0
        while predicate(self._cells):
            self.apply_function(simulator, True)
            self.apply_function_border(border)
            runs += 1
        return runs

    def get_coordinates(self, index: int) -> Iterable[int]:
        if not 0 < index < len(self._cells):
            raise KeyError("Index {0} out of bounds".format(index))
        return self._get_coordinates(index)

    def simulate(self, simulator, border, protocol=None) -> None:
        """
        :param protocol:
        :param simulator:
        :param border:
        :return:
        """
        ncells = [
            (i, simulator([self._focus(x) for x in self.neighbours(i)]))
            for i in self._cell_indices
        ]
        for (i, result) in ncells:
            self._cells[i] = result

        for i in self._border_indices:
            self._cells[i] = border([self._focus(x) for x in self.neighbours(i)])

        if protocol is not None:
            protocol(self._cells)

    def __getitem__(self, index: int) -> T:
        if index is None:
            return None
        if 0 > index >= len(self._cells):
            return None
        else:
            return self._cells[index]

    def __setitem__(self, index: int, value: T) -> None:
        self._cells[index] = value

    @classmethod
    def from_file(cls, filename: str, converter: Callable[[Dict[str, Any]], T]) -> Any:
        grid = CubeGrid()
        with open(filename) as src:
            grid.load(src, converter)
        return grid

    def _get_index(self, coord: Iterable[int]) -> int:
        """
        :param coord:
        :return:
        >>> grid = CubeGrid(4, 3)
        >>> grid._get_index((4, 3))
        >>> grid._get_index((2, 1))
        6

        """
        return sum((c*o for (c, o) in zip(coord, self._offsets))) if self._is_in_bounds(coord) else None

    def _is_in_bounds(self, coord: Iterable[int]) -> bool:
        """
        :param coord:
        :return:
        >>> grid = CubeGrid(3, 4)
        >>> grid._is_in_bounds((0,0))
        True
        >>> grid._is_in_bounds((-1,0))
        False
        >>> grid._is_in_bounds((2,3))
        True
        >>> grid._is_in_bounds((2,4))
        False
        """
        return False not in (
            0 <= c < d
            for (c, d) in
            zip(coord, self._dim)
        )

    def _get_coordinates(self, index: int) -> Iterable[int]:
        """

        :param index:
        :return:
        >>> grid = CubeGrid(4,3)
        >>> grid._get_coordinates(6)
        (2, 1)
        """
        coordinates = []
        for offset in reversed(self._offsets):
            coordinates.append(index // offset)
            index %= offset
        return tuple(reversed(coordinates))

    def _create_layout(self) -> List[Iterable[int]]:
        return map(self._get_coordinates, range(len(self._cells)))

    def _focus(self, indices: Tuple[int, int]) -> Tuple[T, T]:
        """

        :param indices:
        :param dim:
        :return:
        """
        l, u = indices
        return self._cells[l] if l >= 0 else None, self._cells[u] if u < len(self._cells) else None



