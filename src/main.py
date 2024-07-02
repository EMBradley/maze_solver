"""Maze Solver: Generates and solves a maze"""

from gui import Maze, Window


def main():
    """Entry point for maze solver program"""
    window = Window(800, 800)
    Maze(10, 10, 10, 10, 75, 75, window)
    window.wait_for_close()


main()
