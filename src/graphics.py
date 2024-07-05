# pylint: disable=too-few-public-methods
"""Provides graphical interface for maze solver"""
from tkinter import Canvas, Tk


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
        self.__root.title("Maze Solver")
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

    def clear(self):
        """Clears contents of `self`"""
        self.__canvas.delete("all")
