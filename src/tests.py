# pylint: disable=missing-docstring

import unittest
from random import randint

from cell import Direction
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_rows = 50
        num_cols = 100
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(maze.cells), num_rows)
        for j in range(num_rows):
            self.assertEqual(len(maze.cells[j]), num_cols)

    def test_maze_break_entrance_and_exit(self):
        num_rows = 16
        num_cols = 20
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(maze.cells[0][0].walls[Direction.Up])
        self.assertFalse(maze.cells[num_rows - 1][num_cols - 1].walls[Direction.Down])

    def test_solvable(self):
        """Generate 100 mazes of random sizes and check that they have solutions"""
        for _ in range(100):
            num_rows = randint(10, 50)
            num_cols = randint(10, 50)
            maze = Maze(0, 0, num_rows, num_cols, 10, 10)
            self.assertTrue(maze.dfs())
            maze.reset()
            self.assertTrue(maze.bfs())
            maze.reset()
            self.assertTrue(maze.a_star())


if __name__ == "__main__":
    unittest.main()
