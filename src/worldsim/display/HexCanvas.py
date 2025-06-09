import math

from worldsim.display.BaseCanvas import BaseCanvas

class HexCanvas(BaseCanvas):
    def __init__(self, world, parent, cols, rows, cellSize=25):
        self.__centres = {}
        self.hexHeight = math.sqrt(3) * cellSize

        width = cellSize * 3 / 2 * cols + cellSize / 2
        height = self.hexHeight * rows + self.hexHeight / 2

        super().__init__(world, parent, cols, rows, width, height, cellSize)

        self.initGrid()
        self.initPopup()

    def hex_corner(self, cx, cy, size, i):
        deg = 60 * i
        rad = math.radians(deg)
        return cx + size * math.cos(rad), cy + size * math.sin(rad)

    def draw_hex(self, cx, cy, size, fill="white"):
        points = [self.hex_corner(cx, cy, size, i) for i in range(6)]
        return self.create_polygon(points, fill=fill, outline="black")

    def initGrid(self):
        size = self.cellSize
        h = self.hexHeight
        # Top padding so first row isn't cut off
        y_offset = h / 2 - 1

        for row in range(self.rows):
            for col in range(self.cols):
                x = size * 3 / 2 * col
                y = h * row + (h / 2 if col % 2 else 0) + y_offset
                hex = self.draw_hex(x + size, y, size, fill="white")  # only shift x
                label = self.create_text(x + size, y, text="", font=("Arial", 10, "bold"))
                self.cells[(col, row)] = (hex, label)
                self.__centres[(col, row)] = (x + size, y)

    def getClickedHex(self, event):
        minDistance = float("inf")
        clickedCol = clickedRow = None

        for (col, row), (x, y) in self.__centres.items():
            distance = math.hypot(x - event.x, y - event.y)

            if distance <= self.cellSize and distance < minDistance:
                minDistance = distance
                clickedCol = col
                clickedRow = row

        if clickedCol is not None and clickedRow is not None:
            return clickedCol, clickedRow
        return None

    def showPopup(self, event):
        clicked = self.getClickedHex(event)
        if clicked:
            self.clickedCol, self.clickedRow = clicked

            # Only show popup if not occupied
            if not self.world.takenCells[self.clickedCol, self.clickedRow]:
                self.menu.tk_popup(event.x_root, event.y_root)

            # Enable/disable Human option
            if self.world.human is None:
                self.menu.entryconfig(3, state="normal")
            else:
                self.menu.entryconfig(3, state="disabled")