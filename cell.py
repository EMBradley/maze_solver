# pylint: disable=too-many-arguments
"""Provides rectangular cells for drawing maze"""

from typing import Self

from graphics import Line, Point, Window


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
        window: Window | None = None,
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
        self.visited = False

    def get_center(self) -> Point:
        """
        Returns the point in the center of a cell,
        rounding up and to the left
        """
        return Point((self.__x1 + self.__x2) // 2, (self.__y1 + self.__y2) // 2)

    def draw(self) -> None:
        """Draws the cell on the given canvas"""
        assert self.__window is not None

        top_wall = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
        bottom_wall = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
        left_wall = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
        right_wall = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))

        for wall, name in [
            (top_wall, "top"),
            (bottom_wall, "bottom"),
            (left_wall, "left"),
            (right_wall, "right"),
        ]:
            if self.walls[name]:
                fill_color = "black"
            else:
                fill_color = "#d9d9d9"
            self.__window.draw_line(wall, fill_color)

    def draw_move(self, to_cell: Self, undo=False) -> None:
        """
        Draws a line from the center of `self` to the center of `to_cell`
        """
        assert self.__window is not None

        if undo:
            fill_color = "gray"
        else:
            fill_color = "red"
        start = self.get_center()
        end = to_cell.get_center()
        self.__window.draw_line(Line(start, end), fill_color)
