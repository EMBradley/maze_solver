"""Maze Solver: Generates and solves a maze"""

from gui import Line, Point, Window


def main():
    """Entry point for maze solver program"""
    window = Window(800, 800)
    p = Point(2, 2)
    q = Point(800, 800)
    r = Point(2, 800)
    s = Point(800, 2)

    for a, b in [(p, q), (p, r), (p, s), (q, r), (q, s), (r, s)]:
        window.draw_line(Line(a, b))

    window.wait_for_close()


main()
