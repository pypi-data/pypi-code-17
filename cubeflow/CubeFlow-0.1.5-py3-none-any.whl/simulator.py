from typing import Any, Dict, Tuple, Generic, TypeVar, Sequence, Callable, Optional
from types import MethodType
from logging import Logger, ERROR
from itertools import product, count
from cubeflow.cube import CubeGrid
from cubeflow.report import Report, Monitor
from cubeflow.cell import Scalar, MetaCell

CellType = TypeVar('CellType')


def _create_first_derivative(name):
    def derive(self, cells, dimension: int, upper_weight=1.0, lower_weight=0.0, center_weight=1.0):
        higher = cells[tuple(1 if i == dimension else 0 for i in range(self._grid.dimension))]
        center = cells[(0,) * self._grid.dimension]
        lower = cells[tuple(-1 if i == dimension else 0 for i in range(self._grid.dimension))]
        result = upper_weight * getattr(higher, name)
        result -= center_weight * getattr(center, name)
        result += lower_weight * getattr(lower, name)
        result /= self._dls[dimension]
        return result
    return derive


def _create_second_derivative(name):
    def derive_2nd(self, cells, dimension: int, upper_weight=1.0, lower_weight=1.0, center_weight=2.0) -> float:
        higher = cells[tuple(1 if i == dimension else 0 for i in range(self._grid.dimension))]
        lower = cells[tuple(-1 if i == dimension else 0 for i in range(self._grid.dimension))]
        center = cells[(0,) * self._grid.dimension]
        value = upper_weight * getattr(higher, name)
        value -= center_weight * getattr(center, name)
        value += lower_weight * getattr(lower, name)
        return value / self._dls[dimension] ** 2
    return derive_2nd


def _create_laplace(derive_2nd):
    def laplace(self, cells, upper_weight=1.0, lower_weight=1.0, center_weight=2.0) -> float:
        return sum(
            derive_2nd(self, cells, dim, upper_weight, lower_weight, center_weight)
            for dim in range(self._grid.dimension)
        )
    return laplace


def _create_gradient(derive):
    def grad(self, cells, upper_weight=1.0, lower_weight=0.0, center_weight=1.0) -> Sequence[float]:
        return tuple(derive(
            self,
            cells,
            dim,
            upper_weight,
            lower_weight,
            center_weight
        ) for dim in range(self._grid.dimension))
    return grad


def add_derivations(cls):
    """
    
    :param cls: 
    :return:
    >>> class TestCell(metaclass=MetaCell):
    ...     density = Scalar()
    ...     mass = Scalar()
    
    >>> @add_derivations
    ... class TestSimulator(BaseSimulator[TestCell]):
    ...     Type = TestCell
    >>> simulator = TestSimulator(CubeGrid(3, 3))
    >>> left, right, center, up, down = TestCell(0), TestCell(0), TestCell(0), TestCell(0), TestCell(0)
    >>> left.density, right.density, center.density, up.density, down.density = 10.0, 4.0, 2.0, 1.0, 5.0
    >>> cells = {(0, 0): center,(-1, 0): left, (1, 0): right, (0, 1): up, (0, -1): down}
    >>> simulator.derive_density(cells, 0)
    2.0
    >>> simulator.derive_mass(cells, 0)
    0.0
    >>> simulator.grad_density(cells)
    (2.0, -1.0)
    >>> simulator.grad_mass(cells)
    (0.0, 0.0)
    >>> simulator.laplace_density(cells)
    12.0
    >>> simulator.laplace_mass(cells)
    0.0
    """
    scalars = [(name, scalar) for (name, scalar) in cls.Type.__dict__.items() if isinstance(scalar, Scalar)]
    for (name, scalar) in scalars:
        first_derivative = _create_first_derivative(name)
        second_derivative = _create_second_derivative(name)
        laplace = _create_laplace(second_derivative)
        gradient = _create_gradient(first_derivative)

        setattr(cls, 'derive_{0}'.format(name), first_derivative)
        setattr(cls, 'derive2_{0}'.format(name), second_derivative)
        setattr(cls, 'laplace_{0}'.format(name), laplace)
        setattr(cls, 'grad_{0}'.format(name), gradient)

    return cls


class _BorderHandler(Generic[CellType]):
    Template = Dict[Sequence[int], CellType]

    @property
    def handler(self) -> Callable[[Dict[Sequence[int], Any]], Any]:
        return self._handler

    def __init__(self, type_id: int, func: Callable[[Template], CellType]) -> None:
        if type_id == 0:
            raise ValueError("Cell type 0 is reserved for inner cells, not border types.")
        self.border_type = type_id
        self._handler = func

    def __call__(self, cells: Template) -> CellType:
        return self._handler(cells)


class _StabilityCondition(Generic[CellType]):

    def __init__(
            self,
            func: Callable[[CubeGrid[CellType]], Optional[Tuple[int, str]]],
    ) -> None:
        self._func = func

    def __call__(self, grid: CubeGrid) -> Optional[Tuple[int, str]]:
        return self._func(grid)


def border_handler(border_type: int):
    def wrapper(f):
        return _BorderHandler(border_type, f)
    return wrapper


def stability_condition(f):
    return _StabilityCondition(f)


class BaseSimulator(Generic[CellType]):
    Template = Dict[Sequence[int], CellType]
    Type = None

    @property
    def logger(self) -> Optional[Logger]:
        return self._logger

    @logger.setter
    def logger(self, logger: Optional[Logger]) -> None:
        self._logger = logger

    @property
    def dt(self) -> float:
        return self._dt

    @dt.setter
    def dt(self, value: float) -> None:
        self._dt = value

    @property
    def ignore_stability_errors(self) -> bool:
        return self._ignore_stability_errors

    @ignore_stability_errors.setter
    def ignore_stability_errors(self, value: bool) -> None:
        self._ignore_stability_errors = value

    def __init__(
            self,
            grid: CubeGrid[CellType],
            reports: Sequence[Report[CellType]] = [],
            monitors: Sequence[Monitor[CellType]] = [],
            logger: Optional[Logger]=None
    ) -> None:
        self._grid = grid
        self._reports = reports
        self._monitors = monitors
        self._logger = logger
        self._t = 0
        self._dt = 0.1
        self._dls = grid.lengths
        self._ignore_stability_errors = False
        self._orientation = sorted(product((-1, 0, 1), repeat=grid.dimension), key=self._normalise_direction)
        self._border_handlers = dict([
            (handler.border_type, handler.handler)
            for handler in self.__class__.__dict__.values()
            if isinstance(handler, _BorderHandler)
        ])
        self._stability_conditions = [
            condition for condition in self.__dict__.values() if isinstance(condition, _StabilityCondition)
        ]

    def simulate_while(self, predicate: Callable[[Any], bool]) -> None:
        while predicate(self):
            self._grid.apply_function_border(self._border)
            for report in self._reports:
                report(self._grid, self._t)
            for monitor in self._monitors:
                monitor(self._grid)
            for condition in self._stability_conditions:
                result = condition(self._grid)
                if result:
                    if self.logger:
                        self.logger.log(result[0], result[1])
                    if result[0] == ERROR and not self.ignore_stability_errors:
                        raise RuntimeError(result[1])

            self._grid.apply_function(self._prepare, True)
            self._grid.apply_function(self._simulate, True)
            self._t += self._dt

    @classmethod
    def _get_adjacent_inner(cls, cells: Template, orthogonal: bool=True) -> Template:
        return dict(
            (coordinates, cell)
            for (coordinates, cell) in cells.items()
            if cell and cell.type == 0 and (coordinates.count(0) == len(coordinates)-1 if orthogonal else True)
        )

    @classmethod
    def _get_only_cell(cls, cells: Template) -> Tuple[Sequence[int], CellType]:
        single = [
            (coordinates, cell) for (coordinates, cell) in cells.items() if cell
        ]
        if len(single) != 1:
            raise RuntimeError("Requested single only cell, but got {0} cells instead of one".format(len(single)))
        return single[0]

    @classmethod
    def _handle_corner(cls, cells: Template) -> CellType:
        cell = cells[(0, 0)]
        cell.update(next(
            neighbour
            for neighbour in cells.values()
            if neighbour and neighbour.type != 0 and neighbour != cell
        ))
        return cell

    @classmethod
    def _normalise_direction(cls, direction: Sequence[int]) -> float:
        """
        :param direction: 
        :return:
        >>> sorted(product((-1, 0, 1), repeat=2), key=BaseSimulator._normalise_direction)
        [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        """
        return sum(abs(x)*weight - (0.5 if x > 0 else 0) for (x, weight) in zip(direction, count(1)))

    def _align_cells(self, cells: Template) -> Sequence[CellType]:
        return [cells[coordinate] for coordinate in self._orientation]

    def _border(self, cells: Template) -> CellType:
        border_type = cells[(0, 0)].type
        try:
            return self._border_handlers[border_type](self, cells)
        except KeyError:
            raise KeyError("No border handler defined for border type {0}".format(border_type))

    def _simulate(self, cells: Template) -> CellType:
        raise NotImplementedError("BaseSimulator._simulate must be overwritten.")

    def _prepare(self, cells: Template) -> CellType:
        raise NotImplementedError("BaseSimulator._prepare must be overwritten.")





