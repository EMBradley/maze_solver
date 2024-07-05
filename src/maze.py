# pylint: disable=[too-few-public-methods, too-many-arguments, too-many-instance-attributes]
"""Provides class for creating and draw maze"""
import heapq
import random
from time import sleep

from cell import Cell, Direction
from graphics import Window


def opposite_direction(direction: Direction) -> Direction:
    """Returns the direction opposite the one given"""
    match direction:
        case Direction.Up:
            return Direction.Down
        case Direction.Down:
            return Direction.Up
        case Direction.Left:
            return Direction.Right
        case Direction.Right:
            return Direction.Left


class Heap:
    """
    Convenience class for simplifying heapq usage
    """

    def __init__(self, array=None, heapify=True):
        if array:
            self.heap = array
            if heapify:
                heapq.heapify(self.heap)
        else:
            self.heap = []

    def push(self, x):
        """Push item to heap"""
        heapq.heappush(self.heap, x)

    def pop(self):
        """Remove highest priority element from heap"""
        return heapq.heappop(self.heap)


class Maze:
    """Defines the entire maze"""

    def __init__(
        self,
        x: int,
        y: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        window: Window | None = None,
        seed: float | None = None,
        animation_delay: float | None = None,
    ) -> None:
        assert x >= 0
        assert y >= 0
        assert num_rows > 0
        assert num_cols > 0
        assert cell_size_x > 0
        assert cell_size_y > 0

        if seed:
            random.seed(seed)

        self.__x = x
        self.__y = y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__window = window
        self.__animation_delay = animation_delay
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls()
        self.reset()
        self.__draw_cells()

    def __start(self) -> Cell:
        return self.cells[0][0]

    def __end(self) -> Cell:
        return self.cells[-1][-1]

    def __animate(self, factor: float = 1.0) -> None:
        if not self.__window:
            return

        self.__window.redraw()
        if self.__animation_delay and factor:
            sleep(self.__animation_delay * factor)

    def __draw_cells(self) -> None:
        _ = [cell.draw() for row in self.cells for cell in row]
        self.__animate()

    def __undo_path(
        self,
        current_cell: Cell,
        stack: list[tuple[int, int]],
    ) -> None:
        if not stack:
            return

        m, n = stack[-1]
        next_cell = self.cells[m][n]
        branch_cell = next_cell.parent

        draw_cell = current_cell
        while draw_cell != branch_cell and draw_cell.parent:
            draw_cell.draw_move(draw_cell.parent, undo=True)
            draw_cell = draw_cell.parent

    def __create_cells(self) -> None:
        def create_cell(i: int, j: int) -> Cell:
            x1 = self.__x + self.__cell_size_x * j
            y1 = self.__y + self.__cell_size_y * i
            x2 = x1 + self.__cell_size_x
            y2 = y1 + self.__cell_size_y
            cell = Cell(x1, y1, x2, y2, self.__window)
            cell.h_score = self.num_cols - i + self.num_rows - j
            return cell

        self.cells = [
            [create_cell(i, j) for j in range(self.num_cols)]
            for i in range(self.num_rows)
        ]

    def __break_entrance_and_exit(self) -> None:
        entrance_cell = self.cells[0][0]
        exit_cell = self.cells[-1][-1]

        entrance_cell.walls[Direction.Up] = False
        exit_cell.walls[Direction.Down] = False

    def __break_walls(self) -> None:
        start = self.__start()
        start.visited = True
        stack = [(0, 0)]
        came_from = {}

        while stack:
            i, j = stack.pop()
            current_cell = self.cells[i][j]

            if not current_cell.visited and current_cell in came_from:
                parent, direction = came_from[current_cell]
                parent.walls[direction] = False
                current_cell.walls[opposite_direction(direction)] = False

                current_cell.visited = True

            univisited_neighbors = self.__get_unvisited_neighbors(i, j)
            random.shuffle(univisited_neighbors)
            for k, l, direction in univisited_neighbors:
                neighbor = self.cells[k][l]
                came_from[neighbor] = (current_cell, direction)
                stack.append((k, l))

    def reset(self):
        """Resets the state of the maze"""

        def reset_cell(cell: Cell):
            cell.visited = False
            cell.parent = None
            cell.g_score = float("inf")
            cell.f_score = float("inf")

        _ = [reset_cell(cell) for row in self.cells for cell in row]

        if self.__window:
            self.__window.clear()
            self.__draw_cells()

    def __get_neighbor(self, i: int, j: int, direction: Direction):
        match direction:
            case Direction.Down:
                return (i + 1, j, direction)
            case Direction.Up:
                return (i - 1, j, direction)
            case Direction.Right:
                return (i, j + 1, direction)
            case Direction.Left:
                return (i, j - 1, direction)

    def __get_unvisited_neighbors(
        self, i: int, j: int
    ) -> list[tuple[int, int, Direction]]:
        directions = [
            Direction.Down,
            Direction.Right,
            Direction.Up,
            Direction.Left,
        ]

        neighbors = [self.__get_neighbor(i, j, direction) for direction in directions]

        unvisited_neighbors = [
            (k, l, direction)
            for (k, l, direction) in neighbors
            if k in range(self.num_rows)
            and l in range(self.num_cols)
            and not self.cells[k][l].visited
        ]

        return unvisited_neighbors

    def __get_accessible_neighbors(self, i: int, j: int) -> list[tuple[int, int]]:
        current_cell = self.cells[i][j]
        accessible_neighbors = [
            (k, l)
            for (k, l, direction) in self.__get_unvisited_neighbors(i, j)
            if not current_cell.walls[direction]
        ]
        return accessible_neighbors

    def bfs(self) -> bool:
        """
        Solves the maze using breadth first search
        and draws all attempted paths to the screen
        """
        current_cell = self.__start()
        queue = [(0, 0)]
        self.cells[0][0].g_score = 0

        while queue:
            i, j = queue.pop(0)
            current_cell = self.cells[i][j]

            if current_cell == self.__end():
                self.__draw_end_to_start()
                return True

            if current_cell.visited:
                continue

            current_cell.visited = True

            if current_cell.parent:
                current_cell.parent.draw_move(current_cell, undo=True)
                self.__animate(factor=1 / (len(queue) + 1))

            for k, l in self.__get_accessible_neighbors(i, j):
                next_cell = self.cells[k][l]
                next_cell.parent = current_cell
                next_cell.g_score = current_cell.g_score + 1
                queue.append((k, l))

        return False

    def dfs(self) -> bool:
        """
        Solves the maze using recursive depth first search
        and draws all attempted paths to the screen
        """
        stack = [(0, 0)]

        while stack:
            i, j = stack.pop()
            current_cell = self.cells[i][j]

            if current_cell.parent:
                current_cell.draw_move(current_cell.parent)
                self.__animate()

            if not current_cell.visited:
                if current_cell == self.__end():
                    return True
                current_cell.visited = True

            accessible_neighbors = self.__get_accessible_neighbors(i, j)

            if not accessible_neighbors:
                self.__undo_path(current_cell, stack)
                self.__animate()

            for k, l in reversed(self.__get_accessible_neighbors(i, j)):
                neighbor = self.cells[k][l]
                neighbor.parent = current_cell
                stack.append((k, l))

        return False

    def __find_next_branch(self, i: int, j: int, g: float) -> tuple[int, int, float]:
        k, l = i, j
        start_cell = self.cells[k][l]
        if start_cell == self.__end():
            return k, l, g

        current_cell = start_cell
        if current_cell.parent:
            current_cell.draw_move(current_cell.parent, undo=True)

        while len(self.__get_accessible_neighbors(k, l)) == 1:
            k, l = self.__get_accessible_neighbors(k, l)[0]
            next_cell = self.cells[k][l]
            next_cell.parent = current_cell
            current_cell.draw_move(next_cell, undo=True)
            if self.__animation_delay:
                self.__animate(factor=0.25)
            current_cell.visited = True
            current_cell = next_cell
            g += 1

            if next_cell == self.__end():
                return k, l, g

        return k, l, g

    def __draw_end_to_start(self):
        current_cell = self.cells[-1][-1]
        path_length = current_cell.g_score

        if path_length > 1000 or not self.__animation_delay:
            factor = 0
        else:
            factor = 1 / (path_length * self.__animation_delay)

        while current_cell.parent:
            current_cell.draw_move(current_cell.parent)
            current_cell = current_cell.parent
            self.__animate(factor)

    def a_star(self) -> bool:
        """
        Solves the maze using A* search and draws all attempted paths
        """
        start = self.__start()
        start.g_score = 1.0
        start.f_score = start.g_score + start.h_score
        heap = Heap(array=[(start.f_score, 0, 0)])

        while len(heap.heap):
            _, i, j = heap.pop()
            current_cell = self.cells[i][j]
            if current_cell.visited:
                continue
            if current_cell.parent:
                current_cell.draw_move(current_cell.parent, undo=True)
            current_cell.visited = True

            for k, l in self.__get_accessible_neighbors(i, j):
                self.cells[k][l].parent = current_cell
                g_new = current_cell.g_score + 1.0
                (k, l, g_new) = self.__find_next_branch(k, l, g_new)
                next_cell = self.cells[k][l]

                if next_cell == self.__end():
                    self.cells[k][l].g_score = g_new
                    self.__draw_end_to_start()
                    return True

                f_new = g_new + next_cell.h_score
                if f_new < next_cell.f_score:
                    heap.push((f_new, k, l))
                    next_cell.f_score = f_new
                    next_cell.g_score = g_new

            self.__animate()

        return False
