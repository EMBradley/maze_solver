# pylint: disable=too-few-public-methods
"""Classes for creating and interacting with graphical interface"""

from tkinter import Canvas, Tk


class Point:
    """
    A point in a window that is `self.x` pixels from the left edge
    and `self.y pixels from the top
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Line:
    """
    A line segment to be drawn on screen with `self.points` as endpoints
    """

    def __init__(self, point_1: Point, point_2: Point) -> None:
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, canvas: Canvas, fill_color: str = "black") -> None:
        """Draw the line on the provided `Canvas`"""

        canvas.create_line(
            self.point_1.x,
            self.point_1.y,
            self.point_2.x,
            self.point_2.y,
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
