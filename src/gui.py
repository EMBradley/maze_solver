"""Classes for creating and interacting with graphical interface"""

from tkinter import Canvas, Tk


class Window:
    """Graphical interface window"""

    def __init__(self, width, height):
        self.__root = Tk(className="Maze Solver")
        self.__canvas = Canvas(height=height, width=width)
        self.__canvas.pack()
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        """Updates contents of window"""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        """Continuously redraws window until it is closed"""
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        """Closes window"""
        self.__running = False
