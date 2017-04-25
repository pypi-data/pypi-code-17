from typing import List, Tuple, Iterable, Dict, TypeVar, Callable, Generic, Sequence, Any, Union, Optional
from json import load
from itertools import count, product
from operator import mul
from functools import reduce

T = TypeVar('T')

Neighbours = Dict[Sequence[int], T]


def _default_converter(type_: int, **data: Dict[str, float]) -> Dict[str, Union[int, float]]:
    return dict(type=type_, **data)


class CubeGrid(Generic[T]):
    """
    CubeGrid represents a domain of cells: T with any integral dimension. The cell type T should have
    cubeflow.cell.MetaCell as meta class although this is not strictly required for the grid itself.
    Not using cubeflow.cell.MetaCell as meta class of type T only disallows the use of certain simulation 
    helpers, more details can be found in the documentation of the mentioned helpers. 
    """

    @property
    def borders(self) -> List[int]:
        """
        List of all border indices. All border cells have a cell type greater than zero.
        :return: List containing all border indices.
        """
        return list(self._border_indices)

    @property
    def cells(self) -> List[int]:
        """
        List of all inner cell indices (all cells that are not borders).
        :return: List containing all inner cell indices.
        """
        return list(self._cell_indices)

    @property
    def grid(self) -> List[T]:
        """
        Cells of the grid ordered by index. Modification of the grid in this way is possible, although
        not recommended.
        :return: The internal storage containing the grid cells.
        """
        return self._cells

    @property
    def coordinate_system(self) -> Iterable[Tuple[Sequence[float], T]]:
        """
        Generator containing all grid cells by their coordinates as a tuple of the form
        (coordinates, cell).
        :return: Generator with all grid cells referenced by their coordinates.
        """
        return [
            (self._get_coordinates(index), self._cells[index])
            for index in range(len(self._cells))
        ]

    @property
    def layout(self) -> List[Iterable[int]]:
        """
        List of all coordinates of the grid.
        :return: 
        """
        return self._layout

    @property
    def dimension(self) -> int:
        """
        The dimension of the grid, usually 2 or 3 but hyperdimensional cubes are possible, too.
        :return: Dimension of the grid.
        """
        return len(self._dim)

    @property
    def lengths(self) -> Sequence[float]:
        """
        One vector with the same dimension as the grid.
        :return: Sequence containing grid.dimension times 1.0.
        """
        return self._lengths

    def __init__(self, *dimensions: Iterable[int]) -> None:
        """
        Constructs a new CubeGrid object. Actual data cells are delivered to the grid via the load method or by
        modifying the grid cells via the grid property.
        CubeGrid(2, 3, 4) constructs a three dimensional cube with size 2 (x), 3 (y) and 4 (z).
        :param dimensions: Iterable containing the expanses of all dimensions. The length of this parameter is 
        also the dimension of the grid. 
        """
        if dimensions and min(*dimensions) < 0:
            raise ValueError("Length of a dimension must not be negative.")
        self._dim = dimensions
        self._cells = []
        self._border_indices = []
        self._cell_indices = []
        self._offsets = [reduce(mul, dimensions[0:i], 1) for i in range(len(self._dim))]
        self._layout = self._create_layout()
        self._lengths = (1,) * len(self._dim)

    def load(self, buffer, converter=_default_converter) -> None:
        """
        Loads the actual data from a json encoded buffer. Dimensional definitions are retrieved from the file, 
        all present definitions are overwritten. If cell type T has meta class cubeflow.cell.MetaCell, the default 
        value of the converter parameter is always sufficient. For the specification of the data format see README.rst
        or have a look at one of the samples.
        :param buffer: A file like object implementing the buffer protocol that hols the json encoded grid definition.
        :param converter: Function converting the json encoded cell data to the cell type T.
        :return: Nothing
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

    def neighbours(self, index: int) -> Dict[Sequence[int], Optional[int]]:
        """
        Cell indices of all adjacent cells a_i of the specified cell c as a mapping of the form
        vector(c,a_i) -> index(a_i). In the case of a border cell, all direction vectors that step out of the grid
        are mapped to None.
        :param index: Cell index which neighbours should be retrieved.
        :return: Dictionary, mapping direction vectors to cell indices.
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
        """
        Applies a function f, that takes a mapping of directional vectors to grid cells and returns a grid cell, on
        every inner cell c_i of the grid and replaces that cell with its return value (c_i = f(*)). 
        If inner_only parameter is set to false, f is applied to border cells, as well. This method is mainly used
        for calculating secondary or helper values that are stored in the cell in order to be used by the following
        simulation step.
        :param func: The function that should be applied to the grid cells.
        :param inner_only: Specified if f is applied to only inner cells or all cells of the grid.
        :return: 
        """
        for index in self._cell_indices if inner_only else range(len(self._cells)):
            updated = func(self.neighbours(index))
            if not updated:
                raise ValueError("apply_function: func {0} returned None value".format(func))
            self[index] = updated

    def apply_function_border(self, func: Callable[[Neighbours], T]) -> None:
        """
        Same as apply_function, but applies f only to border cells. Will be merged with apply_function in the next
        release.
        :param func: 
        :return: 
        """
        for index in self._border_indices:
            self[index] = func(self.neighbours(index))

    def handle_borders(self, func: Callable[[Neighbours], T]) -> None:
        """
        Same as apply_function, but applies f only to border cells. Will be merged with apply_function in the next
        release.
        :param func: 
        :return: 
        """
        for index in self._border_indices:
            self[index] = func(self.neighbours(index))

    def get_coordinates(self, index: int) -> Iterable[int]:
        """
        The grid coordinates of the cell specified by index.
        :param index: Index of the cell which coordinates should be retrieved.
        :return: Coordinates of the specified cell.
        """
        if not 0 < index < len(self._cells):
            raise KeyError("Index {0} out of bounds".format(index))
        return self._get_coordinates(index)

    def __getitem__(self, index: int) -> Optional[T]:
        """
        Returns the grid cell specified by index if index within bounds, None otherwise.
        :param index: Index of cell which should be retrieved.
        :return: Grid cell object or None.
        """
        if index is None:
            return None
        if 0 > index >= len(self._cells):
            return None
        else:
            return self._cells[index]

    def __setitem__(self, index: int, value: T) -> None:
        """
        Sets the value of a grid cell by index.
        :param index: The index of the new value.
        :param value: Value which overrides the old grid cell at the specified index.
        :return: Nothing.
        """
        self._cells[index] = value

    @classmethod
    def from_file(cls, filename: str, converter: Callable[[Dict[str, Any]], T]=_default_converter) -> Any:
        """
        Creates a new grid by loading and parsing a json file. If cell type T has metaclass cubeflow.cell.MetaCell,
        the default value of the converter parameter is always sufficient. This method makes use of the load method, 
        without the need of creating an object first.
        :param filename: The file to be loaded.
        :param converter: Function that converts json encoded cell data to an object of type T.
        :return: The new CubeGrid object.
        """
        grid = CubeGrid()
        with open(filename) as src:
            grid.load(src, converter)
        return grid

    def _get_index(self, coord: Iterable[int]) -> int:
        """
        Index of a cell referenced by its grid coordinates.
        :param coord: Grid coordinates of the cell.
        :return: Cell index.
        >>> grid = CubeGrid(4, 3)
        >>> grid._get_index((4, 3))
        >>> grid._get_index((2, 1))
        6

        """
        return sum((c*o for (c, o) in zip(coord, self._offsets))) if self._is_in_bounds(coord) else None

    def _is_in_bounds(self, coord: Iterable[int]) -> bool:
        """
        Checks if given grid coordinates are withing bounds regarding the grid.
        :param coord: Grid coordinates.
        :return: True if coordinates are within bounds, False otherwise.
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
        The grid coordinates of the cell specified by index. No boundary checks are performed here.
        :param index: Index of the cell which coordinates should be retrieved.
        :return: Coordinates of the specified cell.
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
        """
        Creates the layout of the grid. 
        :return: List of all grid coordinates of the grid.
        """
        return map(self._get_coordinates, range(len(self._cells)))

    def _focus(self, indices: Tuple[int, int]) -> Tuple[Optional[T], Optional[T]]:
        """
        Maps two cell indices, normally in the same dimension and of distance 2 to the corresponding grid cells.
        :param indices: The indices of the cells to be mapped.
        :return: Tuple containing the grid cells, if such a cell does not exists, its value is None.
        """
        l, u = indices
        return self._cells[l] if l >= 0 else None, self._cells[u] if u < len(self._cells) else None



