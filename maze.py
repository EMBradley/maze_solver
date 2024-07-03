# pylint: disable=[too-few-public-methods, too-many-arguments, too-many-instance-attributes]
"""Provides class for creating and draw maze"""
import random
from time import sleep

from cell import Cell, Direction
from graphics import Window


def opposite_direction(direction: Direction) -> Direction:
    """Returns the direction opposite the one given"""
    match direction:
        case Direction.Up:
            return Direction.Down
        case Direction.Down:
            return Direction.Up
        case Direction.Left:
            return Direction.Right
        case Direction.Right:
            return Direction.Left
        case _:
            raise ValueError


class Maze:
    """Defines the entire maze"""

    def __init__(
        self,
        x: int,
        y: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        window: Window | None = None,
        seed: float | None = None,
        animation_delay: float = 0.0,
    ) -> None:
        assert x >= 0
        assert y >= 0
        assert num_rows > 0
        assert num_cols > 0
        assert cell_size_x > 0
        assert cell_size_y > 0

        if seed:
            random.seed(seed)

        self.__x = x
        self.__y = y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__window = window
        self.__animation_delay = animation_delay
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls()
        self.__reset_cells_visited()
        self.__draw_cells()

    def __animate(self) -> None:
        if not self.__window:
            return

        self.__window.redraw()
        if self.__animation_delay:
            sleep(self.__animation_delay)

    def __draw_cells(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.draw()
        self.__animate()

    def __draw_path(self, path: list[Cell], undo: bool = False) -> None:
        for i in range(len(path) - 1):
            path[i].draw_move(path[i + 1], undo)

    def __undo_path(
        self,
        paths: dict[Cell, list[Cell]],
        current_cell: Cell,
        stack: list[tuple[int, int]],
    ) -> None:
        if not stack:
            return

        current_path = paths[current_cell]
        m, n = stack[-1]
        next_cell = self.cells[m][n]
        next_path = paths[next_cell]
        branch_cell = next_path[-2]
        branch_index = current_path.index(branch_cell)
        self.__draw_path(current_path[branch_index:], undo=True)

    def __create_cells(self) -> None:
        self.cells = []

        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                x1 = self.__x + self.__cell_size_x * j
                y1 = self.__y + self.__cell_size_y * i
                x2 = x1 + self.__cell_size_x
                y2 = y1 + self.__cell_size_y
                cell = Cell(x1, y1, x2, y2, self.__window)
                row.append(cell)
            self.cells.append(row)

    def __break_entrance_and_exit(self) -> None:
        entrance_cell = self.cells[0][0]
        exit_cell = self.cells[-1][-1]

        entrance_cell.walls[Direction.Up] = False
        exit_cell.walls[Direction.Down] = False

    def __break_walls(self) -> None:
        start = self.cells[0][0]
        start.visited = True
        stack = [(0, 0)]
        paths = {start: [(start, Direction.Down)]}

        while stack:
            i, j = stack.pop()
            current_cell = self.cells[i][j]
            current_path = paths[current_cell]

            if not current_cell.visited and len(current_path) > 1:
                previous_cell = current_path[-2][0]
                direction_from_previous = current_path[-1][1]

                previous_cell.walls[direction_from_previous] = False
                current_cell.walls[opposite_direction(direction_from_previous)] = False

                current_cell.visited = True

            univisited_neighbors = self.__get_unvisited_neighbors(i, j)
            random.shuffle(univisited_neighbors)
            for k, l, direction in univisited_neighbors:
                neighbor = self.cells[k][l]
                paths[neighbor] = current_path + [(neighbor, direction)]
                stack.append((k, l))

    def __reset_cells_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def __get_unvisited_neighbors(
        self, i: int, j: int
    ) -> list[tuple[int, int, Direction]]:
        directions_to_check = [
            (i + 1, j, Direction.Down),
            (i, j + 1, Direction.Right),
            (i - 1, j, Direction.Up),
            (i, j - 1, Direction.Left),
        ]

        unvisited_neighbors = []

        for k, l, direction in directions_to_check:
            if k not in range(self.num_rows):
                continue
            if l not in range(self.num_cols):
                continue
            if self.cells[k][l].visited:
                continue
            unvisited_neighbors.append((k, l, direction))

        return unvisited_neighbors

    def __get_accessible_neighbors(self, i: int, j: int) -> list[tuple[int, int]]:
        current_cell = self.cells[i][j]

        unvisited_neighbors = self.__get_unvisited_neighbors(i, j)
        accessible_neighbors = []

        for k, l, direction in unvisited_neighbors:
            if current_cell.walls[direction]:
                continue
            if self.cells[k][l].visited:
                continue
            accessible_neighbors.append((k, l))

        return accessible_neighbors

    def bfs(self) -> bool:
        """
        Solves the maze using breadth first search
        and draws all attempted paths to the screen
        """
        start = self.cells[0][0]
        end = self.cells[-1][-1]
        paths = {start: [start]}
        to_visit = [(0, 0)]

        while to_visit:
            i, j = to_visit.pop(0)
            current_cell = self.cells[i][j]
            current_cell.visited = True
            current_path = paths[current_cell]

            # Draw the last step of the current_path
            if len(current_path) > 1:
                previous_cell = current_path[-2]
                previous_cell.draw_move(current_cell, undo=True)
                self.__animate()

            for k, l in self.__get_accessible_neighbors(i, j):
                next_cell = self.cells[k][l]
                if next_cell == end:
                    current_cell.draw_move(end, undo=True)
                    path_to_end = current_path + [next_cell]
                    self.__draw_path(path_to_end)
                    self.__animate()
                    return True
                if next_cell not in to_visit and next_cell not in paths:
                    to_visit.append((k, l))
                    paths[next_cell] = current_path + [next_cell]

        return False

    def dfs(self) -> bool:
        """
        Solves the maze using recursive depth first search
        and draws all attempted paths to the screen
        """
        start = self.cells[0][0]
        stack = [(0, 0)]
        paths = {start: [start]}

        while stack:
            self.__animate()
            i, j = stack.pop()
            current_cell = self.cells[i][j]
            current_path = paths[current_cell]

            if len(current_path) > 1:
                previous_cell = current_path[-2]
                previous_cell.draw_move(current_cell)

            if not current_cell.visited:
                if current_cell == self.cells[-1][-1]:
                    return True
                current_cell.visited = True

            accessible_neighbors = self.__get_accessible_neighbors(i, j)

            if not accessible_neighbors:
                self.__undo_path(paths, current_cell, stack)
                self.__animate()

            for k, l in reversed(self.__get_accessible_neighbors(i, j)):
                neighbor = self.cells[k][l]
                paths[neighbor] = current_path + [neighbor]
                stack.append((k, l))

        return False
