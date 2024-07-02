"""Maze Solver: Generates and solves a maze"""

from gui import Cell, Window


def main():
    """Entry point for maze solver program"""
    window = Window(800, 800)
    first = Cell(250, 250, 275, 275)
    second = Cell(275, 250, 300, 275)

    window.draw_cell(first)
    window.draw_cell(second)
    window.draw_move(first, second)
    window.wait_for_close()


main()
