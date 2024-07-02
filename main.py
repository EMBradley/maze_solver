"""Maze Solver: Generates and solves a maze"""

from graphics import Window
from maze import Maze


def main():
    """Entry point for maze solver program"""
    cell_size = 25
    num_rows = 35
    num_cols = 35
    padding = 10
    height = num_rows * cell_size + 2 * padding
    width = num_cols * cell_size + 2 * padding
    window = Window(width, height)
    maze = Maze(padding, padding, num_rows, num_cols, cell_size, cell_size, window)
    maze.solve()
    window.wait_for_close()


if __name__ == "__main__":
    main()
