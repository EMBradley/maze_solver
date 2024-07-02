# pylint: disable=too-few-public-methods
"""Classes for creating and interacting with graphical interface"""

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
        # is_finish: bool = False,
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
        # self.__is_finish = is_finish

    def get_center(self):
        """
        Returns the point in the center of a cell,
        rounding up and to the left
        """
        return Point((self.__x1 + self.__x2) // 2, (self.__y1 + self.__y2) // 2)

    def draw(self, canvas: Canvas, fill_color: str = "black"):
        """Draws the cell on the given canvas"""
        if self.walls["top"]:
            top_wall = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
            top_wall.draw(canvas, fill_color)
        if self.walls["bottom"]:
            bottom_wall = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
            bottom_wall.draw(canvas, fill_color)
        if self.walls["left"]:
            left_wall = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
            left_wall.draw(canvas, fill_color)
        if self.walls["right"]:
            right_wall = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
            right_wall.draw(canvas, fill_color)

    def draw_move(self, to_cell: Self, canvas: Canvas, undo=False):
        """
        Draws a line from the center of `self` to the center of `to_cell`
        """
        if undo:
            fill_color = "gray"
        else:
            fill_color = "red"
        start = self.get_center()
        end = to_cell.get_center()
        Line(start, end).draw(canvas, fill_color)


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

    def draw_cell(self, cell: Cell, fill_color: str = "black"):
        """Draw a given cell on the screen"""
        cell.draw(self.__canvas, fill_color)

    def draw_move(self, first_cell: Cell, second_cell: Cell, undo=False):
        """Draw a line between the centers of the given cells"""
        first_cell.draw_move(second_cell, self.__canvas, undo)
