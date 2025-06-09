from typing import override

from worldsim.display.BaseCanvas import BaseCanvas


class SquareCanvas(BaseCanvas):
    def __init__(self, world, parent, cols, rows, cellSize=40):
        height = rows * cellSize
        width = cols * cellSize

        super().__init__(world, parent, cols, rows, width + 4, height + 4, cellSize)

    @override
    def initGrid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cellSize
                y1 = row * self.cellSize
                x2 = x1 + self.cellSize
                y2 = y1 + self.cellSize

                rect = self.create_rectangle(x1, y1, x2, y2, fill="white")
                label = self.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="", font=("Arial", 12, "bold"))

                self.cells[(col, row)] = (rect, label)

    @override
    def showPopup(self, event):
        self.clickedCol = event.x // self.cellSize
        self.clickedRow = event.y // self.cellSize

        # Check if cell is occupied
        if not self.world.takenCells[self.clickedCol, self.clickedRow]:
            self.menu.tk_popup(event.x_root, event.y_root)

        # Check if Human exists
        if self.world.human is None:
            self.menu.entryconfig(3, state="normal")
        else:
            self.menu.entryconfig(3, state="disabled")