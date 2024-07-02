from graphics import Window
from maze import Maze


def main():
    """Entry point for maze solver program"""
    window = Window(800, 800)
    Maze(10, 10, 10, 10, 75, 75, window)
    window.wait_for_close()


if __name__ == "__main__":
    main()
