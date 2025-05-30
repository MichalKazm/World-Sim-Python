import tkinter as tk

from worldsim.display.GameCanvas import GameCanvas


class World:
    def __init__(self, rows, cols):
        self.__rows = rows
        self.__cols = cols
        self.__order = []
        self.__window = tk.Tk()

        self.initWindow()

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    def addOrganism(self, organism):
        if 0 <= organism.y < self.rows and 0 <= organism.x < self.cols:
            organism.world = self
            self.__order.append(organism)
            return True
        else:
            return False

    def getOrganism(self, y, x):
        for organism in self.__order:
            if organism.alive and organism.y == y and organism.x == x:
                return organism

        return None

    def sortOrder(self):
        self.__order.sort(key=lambda organism : (organism.initiative, organism.age), reverse=True)

    def center(self):
        window = self.__window

        window.update_idletasks()

        width = window.winfo_width()
        height = window.winfo_height()

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

    def initWindow(self):
        window = self.__window
        # Initialize windows
        window.title("Simulator")
        window.protocol("WM_DELETE_WINDOW", self.__window.destroy)
        window.resizable(False, False)

        # Initialize game grid
        gameGrid = GameCanvas(window, self.rows, self.cols)
        gameGrid.pack()

        self.center()
        window.mainloop()
