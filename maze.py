# pylint: disable=[too-few-public-methods, too-many-arguments, too-many-instance-attributes]
"""Provides class for creating and draw maze"""
import random
from time import sleep

from cell import Cell
from graphics import Window


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
        seed: int | None = None,
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
        self.__create_cells()
        self.__break_entrance_and_entrance()
        self.__break_walls_recursive(0, 0)
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

    def __draw_cell(self, cell: Cell) -> None:
        cell.draw()
        self.__animate()

    def __animate(self) -> None:
        assert self.__window is not None
        self.__window.redraw()
        sleep(0.03)

    def break_wall(self, cell: Cell, wall: str) -> None:
        """Removes the designated wall, then redraws the cell on screen"""
        cell.walls[wall] = False

        if self.__window:
            self.__draw_cell(cell)

    def __break_entrance_and_entrance(self) -> None:
        entrance_cell = self.cells[0][0]
        exit_cell = self.cells[-1][-1]

        self.break_wall(entrance_cell, "top")
        self.break_wall(exit_cell, "bottom")

    def __break_walls_recursive(self, i: int, j: int) -> None:
        current_cell = self.cells[i][j]
        current_cell.visited = True

        while True:
            to_visit = []

            for k, l in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                if k not in range(self.num_rows) or l not in range(self.num_cols):
                    continue
                if not self.cells[k][l].visited:
                    to_visit.append((k, l))

            if not to_visit:
                return

            (k, l) = random.choice(to_visit)
            next_cell = self.cells[k][l]

            if k > i:
                self.break_wall(current_cell, "bottom")
                self.break_wall(next_cell, "top")
            elif i > k:
                self.break_wall(current_cell, "top")
                self.break_wall(next_cell, "bottom")
            elif l > j:
                self.break_wall(current_cell, "right")
                self.break_wall(next_cell, "left")
            else:
                self.break_wall(current_cell, "left")
                self.break_wall(next_cell, "right")

            self.__break_walls_recursive(k, l)

    def __reset_cells_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False
