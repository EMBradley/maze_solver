"""Maze Solver: Generates and solves a maze"""

from graphics import Window
from maze import Maze


def main():
    """Entry point for maze solver program"""
    cell_size = 40
    num_rows = 15
    num_cols = 15
    padding = 10
    height = num_rows * cell_size + 2 * padding
    width = num_cols * cell_size + 2 * padding
    window = Window(width, height)
    Maze(padding, padding, num_rows, num_cols, cell_size, cell_size, window)
    window.wait_for_close()


if __name__ == "__main__":
    main()
