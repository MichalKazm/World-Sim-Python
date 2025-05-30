import tkinter as tk

class GameCanvas(tk.Canvas):
    def __init__(self, parent, rows, cols, cell_size=25):
        width = cols * cell_size
        height = rows * cell_size
        super().__init__(parent, width=width + 4, height=height + 4, bg="black", highlightthickness=0)

        self.__rows = rows
        self.__cols = cols
        self.__cell_size = cell_size
        self.__cells = {}

        self.drawGrid()

    def drawGrid(self):
        for y in range(self.__rows):
            for x in range(self.__cols):
                x1 = x * self.__cell_size
                y1 = y * self.__cell_size
                x2 = x1 + self.__cell_size
                y2 = y1 + self.__cell_size
                rect = self.create_rectangle(x1, y1, x2, y2, fill="white", )

                self.__cells[(x, y)] = rect