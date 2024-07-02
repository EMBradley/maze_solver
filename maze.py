# pylint: disable=[too-few-public-methods, too-many-arguments, too-many-instance-attributes]
"""Provides class for creating and draw maze"""
import random
from time import sleep

from cell import Cell, Direction
from graphics import Window


def __opposite_direction(direction: Direction) -> Direction:
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
        animation_delay_ms: int = 0,
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
        self.__animation_delay = animation_delay_ms
        self.__create_cells()
        self.__break_entrance_and_entrance()
        self.__break_walls()
        self.__reset_cells_visited()

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

        if not self.__window:
            return

        for row in self.cells:
            for cell in row:
                cell.draw()

    def __animate(self) -> None:
        if not self.__window:
            return

        self.__window.redraw()
        if self.__animation_delay:
            sleep(self.__animation_delay / 1000)

    def __break_wall(self, cell: Cell, wall: Direction) -> None:
        cell.walls[wall] = False
        cell.draw()

    def __break_entrance_and_entrance(self) -> None:
        entrance_cell = self.cells[0][0]
        exit_cell = self.cells[-1][-1]

        self.__break_wall(entrance_cell, Direction.Up)
        self.__break_wall(exit_cell, Direction.Down)

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

                self.__break_wall(previous_cell, direction_from_previous)
                self.__break_wall(
                    current_cell, __opposite_direction(direction_from_previous)
                )

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
        paths = {start: [start]}
        to_visit = [(0, 0)]

        while to_visit:
            i, j = to_visit.pop(0)
            current_cell = self.cells[i][j]
            current_cell.visited = True
            current_path = paths[current_cell]

            # Draw the last step of the current_path
            if len(current_path) > 1:
                current_path[-2].draw_move(current_cell, undo=True)
                self.__animate()

            for k, l in self.__get_accessible_neighbors(i, j):
                next_cell = self.cells[k][l]
                if k + 1 == self.num_rows and l + 1 == self.num_cols:
                    current_cell.draw_move(self.cells[-1][-1], undo=True)
                    path_to_end = current_path + [next_cell]

                    # Redraw the whole correct path in red
                    for a, b in zip(path_to_end[:-1], path_to_end[1:]):
                        a.draw_move(b)
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
        return self.__dfs_recursive(0, 0)

    def __dfs_recursive(self, i: int, j: int) -> bool:
        self.__animate()

        if i + 1 == self.num_rows and j + 1 == self.num_cols:
            return True

        current_cell = self.cells[i][j]
        current_cell.visited = True

        accessible_neighbors = self.__get_accessible_neighbors(i, j)

        for k, l in accessible_neighbors:
            next_cell = self.cells[k][l]
            current_cell.draw_move(next_cell)
            if self.__dfs_recursive(k, l):
                return True
            current_cell.draw_move(next_cell, undo=True)

        return False
