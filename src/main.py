"""Maze Solver: Generates and solves a maze"""

from gui import Cell, Window


def main():
    """Entry point for maze solver program"""
    window = Window(800, 800)
    cell = Cell(250, 250, 275, 275)

    window.draw_cell(cell)
    window.wait_for_close()


main()
