# pylint: disable=[too-few-public-methods, too-many-arguments, too-many-instance-attributes]
"""Maze Solver: Generates and solves a maze"""
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
    ) -> None:
        assert x >= 0
        assert y >= 0
        assert num_rows > 0
        assert num_cols > 0
        assert cell_size_x > 0
        assert cell_size_y > 0

        self.x = x
        self.y = y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.__create_cells()
        self.__break_entrance_and_entrance()

    def __create_cells(self) -> None:
        self.cells = []

        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                x1 = self.x + self.cell_size_x * i
                y1 = self.y + self.cell_size_y * j
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y
                cell = Cell(x1, y1, x2, y2, self.window)
                row.append(cell)
            self.cells.append(row)

        if not self.window:
            return

        for j in range(self.num_cols):
            for i in range(self.num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i: int, j: int) -> None:
        self.cells[i][j].draw()
        self.__animate()

    def __animate(self):
        assert self.window is not None
        self.window.redraw()
        sleep(0.03)

    def __break_entrance_and_entrance(self):
        entrance_cell = self.cells[0][0]
        exit_cell = self.cells[-1][-1]

        entrance_cell.walls["top"] = False
        exit_cell.walls["bottom"] = False

        if not self.window:
            return

        self.__draw_cell(0, 0)
        self.__draw_cell(-1, -1)
