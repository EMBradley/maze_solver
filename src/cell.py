# pylint: disable=[too-many-arguments, too-many-instance-attributes]
"""Provides rectangular cells for drawing maze"""

from enum import Enum
from typing import Self

from graphics import Line, Point, Window

Direction = Enum("Direction", ["Up", "Down", "Left", "Right"])


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
            Direction.Up: True,
            Direction.Down: True,
            Direction.Left: True,
            Direction.Right: True,
        }
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__window = window
        self.visited = False
        self.g_score = float("inf")
        self.h_score = 0.0
        self.f_score = float("inf")
        self.parent: Cell | None = None

    def get_center(self) -> Point:
        """
        Returns the point in the center of a cell,
        rounding up and to the left
        """
        return Point((self.__x1 + self.__x2) // 2, (self.__y1 + self.__y2) // 2)

    def draw(self) -> None:
        """Draws the cell on the given canvas"""
        if not self.__window:
            return

        top_wall = (
            Line(Point(self.__x1 - 1, self.__y1), Point(self.__x2 + 1, self.__y1)),
            Direction.Up,
        )
        bottom_wall = (
            Line(Point(self.__x1 - 1, self.__y2), Point(self.__x2 + 1, self.__y2)),
            Direction.Down,
        )
        left_wall = (
            Line(Point(self.__x1, self.__y1 - 1), Point(self.__x1, self.__y2 + 1)),
            Direction.Left,
        )
        right_wall = (
            Line(Point(self.__x2, self.__y1 - 1), Point(self.__x2, self.__y2 + 1)),
            Direction.Right,
        )

        walls = [top_wall, bottom_wall, left_wall, right_wall]
        broken_walls = [
            wall for (wall, direction) in walls if not self.walls[direction]
        ]
        intact_walls = [wall for (wall, direction) in walls if self.walls[direction]]

        for wall in broken_walls:
            self.__window.draw_line(wall, "#d9d9d9")
        for wall in intact_walls:
            self.__window.draw_line(wall, "black")

    def draw_move(self, to_cell: Self, undo=False) -> None:
        """
        Draws a line from the center of `self` to the center of `to_cell`
        """
        if not self.__window:
            return

        if undo:
            fill_color = "gray"
        else:
            fill_color = "red"
        start = self.get_center()
        end = to_cell.get_center()
        self.__window.draw_line(Line(start, end), fill_color)
