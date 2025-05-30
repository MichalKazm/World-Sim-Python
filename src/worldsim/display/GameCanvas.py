import tkinter as tk

class GameCanvas(tk.Canvas):
    def __init__(self, parent, cols, rows, cell_size=25):
        height = rows * cell_size
        width = cols * cell_size
        super().__init__(parent, width=width + 4, height=height + 4, bg="black", highlightthickness=0)

        self.__cols = cols
        self.__rows = rows
        self.__cell_size = cell_size
        self.__cells = {}

        self.initGrid()

    def initGrid(self):
        for y in range(self.__rows):
            for x in range(self.__cols):
                x1 = x * self.__cell_size
                y1 = y * self.__cell_size
                x2 = x1 + self.__cell_size
                y2 = y1 + self.__cell_size

                rect = self.create_rectangle(x1, y1, x2, y2, fill="white")
                label = self.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="", font=("Arial", 10, "bold"))

                self.__cells[(x, y)] = (rect, label)

    def clear(self):
        for rect, label in self.__cells.values():
            self.itemconfig(rect, fill="white")
            self.itemconfig(label, text="")

    def draw(self, order):
        for organism in order:
            if organism.alive:
                rect, label = self.__cells[(organism.x, organism.y)]

                self.itemconfig(rect, fill=organism.color)
                self.itemconfig(label, text=organism.symbol)