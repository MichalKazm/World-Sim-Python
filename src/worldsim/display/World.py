import tkinter as tk

from worldsim.display.GameCanvas import GameCanvas


class World:
    def __init__(self, cols, rows):
        self.__cols = cols
        self.__rows = rows
        self.__turn = 0
        self.__order = []
        self.takenCells = {}
        self.__window = tk.Tk()
        self.__gameGrid = GameCanvas(self.__window, self.cols, self.rows)

        for x in range(cols):
            for y in range(rows):
                self.takenCells[(x, y)] = False

        self.initWindow()

    @property
    def cols(self):
        return self.__cols

    @property
    def rows(self):
        return self.__rows

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
        # Initialize window
        window.title("Simulator")
        window.protocol("WM_DELETE_WINDOW", self.__window.destroy)
        window.resizable(False, False)

        # Initialize game grid
        self.__gameGrid.pack()

        # Initialize button frame
        buttonFrame = tk.Frame(window)
        buttonFrame.pack(fill="x")

        nextTurnButton = tk.Button(buttonFrame, text="Next turn", command=self.takeTurn)
        nextTurnButton.pack(side="right")

        self.center()

    def run(self):
        self.updateGame()
        self.__window.mainloop()

    def addOrganism(self, organism):
        if 0 <= organism.x < self.cols and 0 <= organism.y < self.rows:
            organism.world = self
            self.__order.append(organism)
            self.takenCells[(organism.x, organism.y)] = True
            return True
        else:
            return False

    def getOrganism(self, x, y):
        for organism in self.__order:
            if organism.alive and organism.x == x and organism.y == y:
                return organism

        return None

    def removeDead(self):
        alive = []
        for organism in self.__order:
            if organism.alive:
                alive.append(organism)

        self.__order = alive

    def sortOrder(self):
        self.__order.sort(key=lambda organism : (organism.initiative, organism.age), reverse=True)

    def updateGame(self):
        game = self.__gameGrid

        game.clear()
        game.draw(self.__order)

    def takeTurn(self):
        self.sortOrder()

        # Number of organisms before the turn
        n = len(self.__order)
        # Only organisms that are alive and created before the turn will take action
        for i in range(n):
            organism = self.__order[i]

            if organism.alive:
                organism.action()

        self.removeDead()
        self.updateGame()
        self.__turn += 1