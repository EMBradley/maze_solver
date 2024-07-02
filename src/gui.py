# pylint: disable=[too-few-public-methods, too-many-arguments]
"""Classes for creating and interacting with graphical interface"""

from time import sleep
from tkinter import Canvas, Tk
from typing import Self


class Point:
    """
    Defines a point on screen at coordintes `x`, `y`,
    measured from the top left of the window
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Line:
    """
    Defines a line on the screen by its endpoints
    """

    def __init__(self, point_1: Point, point_2: Point) -> None:
        self.__point_1 = point_1
        self.__point_2 = point_2

    def draw(self, canvas: Canvas, fill_color: str = "black") -> None:
        """Draw the line on the provided `Canvas`"""

        canvas.create_line(
            self.__point_1.x,
            self.__point_1.y,
            self.__point_2.x,
            self.__point_2.y,
            fill=fill_color,
            width=2,
        )


class Window:
    """Graphical interface window"""

    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk(className="Maze Solver")
        self.__canvas = Canvas(height=height, width=width)
        self.__canvas.pack()
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        """Updates contents of window"""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        """Keeps window open and continuously redraws it until it is closed"""
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self) -> None:
        """Closes window"""
        self.__running = False

    def draw_line(self, line: Line, fill_color: str = "black"):
        """Draw a given line on the screen"""
        line.draw(self.__canvas, fill_color)


class Cell:
    """
    Defines a cell in the maze. The coordinates `x1` and `y1` are its top left corner.
    The coordinates `x2` and `y2` are its bottom right corner
    """

    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        window: Window,
    ) -> None:
        self.walls = {
            "top": True,
            "bottom": True,
            "left": True,
            "right": True,
        }
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__window = window

    def get_center(self):
        """
        Returns the point in the center of a cell,
        rounding up and to the left
        """
        return Point((self.__x1 + self.__x2) // 2, (self.__y1 + self.__y2) // 2)

    def draw(self):
        """Draws the cell on the given canvas"""
        if self.walls["top"]:
            top_wall = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
            self.__window.draw_line(top_wall)
        if self.walls["bottom"]:
            bottom_wall = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
            self.__window.draw_line(bottom_wall)
        if self.walls["left"]:
            left_wall = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
            self.__window.draw_line(left_wall)
        if self.walls["right"]:
            right_wall = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
            self.__window.draw_line(right_wall)

    def draw_move(self, to_cell: Self, undo=False):
        """
        Draws a line from the center of `self` to the center of `to_cell`
        """
        if undo:
            fill_color = "gray"
        else:
            fill_color = "red"
        start = self.get_center()
        end = to_cell.get_center()
        self.__window.draw_line(Line(start, end), fill_color)


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
        window: Window,
    ) -> None:
        self.top_left = (x, y)
        self.dimensions = (num_rows, num_cols)
        self.cell_size = (cell_size_x, cell_size_y)
        self.window = window
        self.__create_cells()

    def __create_cells(self) -> None:
        self.__cells = []

        for j in range(self.dimensions[1]):
            column = []
            for i in range(self.dimensions[0]):
                x1 = self.top_left[0] + self.cell_size[0] * i
                y1 = self.top_left[1] + self.cell_size[1] * j
                x2 = x1 + self.cell_size[0]
                y2 = y1 + self.cell_size[1]
                cell = Cell(x1, y1, x2, y2, self.window)
                column.append(cell)
            self.__cells.append(column)

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                self.__draw_cell(i, j)

    def __draw_cell(self, i: int, j: int) -> None:
        self.__cells[i][j].draw()
        self.__animate()

    def __animate(self):
        self.window.redraw()
        sleep(0.05)
