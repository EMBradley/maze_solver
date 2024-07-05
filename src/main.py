"""Maze Solver: Generates and solves a maze"""

import sys
from time import sleep

from graphics import Window
from maze import Maze


def main():
    """Entry point for maze solver program"""
    num_rows = __get_input("Number of rows:    ")
    num_cols = __get_input("Number of columns: ")
    cell_size = __get_input("Cell size:         ")
    # algorithm = __get_input("Algorithm: (1) for DFS, (2) for BFS, (3) for A*\n")

    padding = 10
    height = num_rows * cell_size + 2 * padding
    width = num_cols * cell_size + 2 * padding
    window = Window(width, height)
    animation_delay = 1 / (height * width)

    maze = Maze(
        padding,
        padding,
        num_rows,
        num_cols,
        cell_size,
        cell_size,
        window,
        animation_delay=animation_delay,
    )

    maze.dfs()
    sleep(5)
    maze.reset()
    maze.bfs()
    sleep(5)
    maze.reset()
    maze.a_star()
    # match algorithm:
    #     case 1:
    #         maze.dfs()
    #     case 2:
    #         maze.bfs()
    #     case 3:
    #         maze.a_star()

    window.wait_for_close()


def __get_input(prompt: str) -> int:
    while True:
        string = input(prompt)
        if string.lower() == "q":
            sys.exit()
        try:
            return int(string)
        except ValueError:
            print(f"Invalid input {string}. Please try again.\n")


if __name__ == "__main__":
    main()
