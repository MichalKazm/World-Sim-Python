import tkinter as tk

from worldsim.animals.Antelope import Antelope
from worldsim.animals.CyberSheep import CyberSheep
from worldsim.animals.Fox import Fox
from worldsim.animals.Human import Human
from worldsim.animals.Sheep import Sheep
from worldsim.animals.Turtle import Turtle
from worldsim.animals.Wolf import Wolf
from worldsim.display.GameCanvas import GameCanvas
from worldsim.plants.Dandelion import Dandelion
from worldsim.plants.DeadlyNightshade import DeadlyNightshade
from worldsim.plants.Grass import Grass
from worldsim.plants.Guarana import Guarana
from worldsim.plants.Hogweed import Hogweed


class World:
    def __init__(self, cols, rows):
        self.__cols = cols
        self.__rows = rows
        self.__turn = 1
        self.__human = None
        self.__order = []
        self.takenCells = {}
        self.hogweedMap = {}
        self.__window = tk.Tk()
        self.__gameGrid = None
        self.__logs = None

        for x in range(cols):
            for y in range(rows):
                self.takenCells[(x, y)] = False
                self.hogweedMap[(x, y)] = False

        self.initWindow()

        self.appendLog("-- Turn 0 --")

    @property
    def cols(self):
        return self.__cols

    @property
    def rows(self):
        return self.__rows

    @property
    def human(self):
        return self.__human

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

        # Initialize main frame
        mainFrame = tk.Frame(window)
        mainFrame.pack(fill="both")

        # Initialize game grid
        self.__gameGrid = GameCanvas(self, mainFrame, self.cols, self.rows)
        self.__gameGrid.pack(side="left")

        # Initialize logs
        logFrame = tk.Frame(mainFrame)
        logFrame.pack(side="right", fill="both")

        # Initialize scrollbar
        scrollbar = tk.Scrollbar(logFrame)
        scrollbar.pack(side="right", fill="y")

        # Initialize text for logs
        self.__logs = tk.Text(logFrame, yscrollcommand=scrollbar.set, wrap="word", font=("Serif", 10) , width=50, state="disabled")
        self.__logs.pack(side="left", fill="both")

        scrollbar.config(command=self.__logs.yview)


        # Initialize button frame
        buttonFrame = tk.Frame(window)
        buttonFrame.pack(fill="x")

        nextTurnButton = tk.Button(buttonFrame, text="Next turn", command=self.takeTurn)
        nextTurnButton.pack(side="right")

        loadButton = tk.Button(buttonFrame, text="Load", command=self.load)
        loadButton.pack(side="right")

        saveButton = tk.Button(buttonFrame, text="Save", command=self.save)
        saveButton.pack(side="right")

        # Bind keys to actions
        window.bind("<w>", lambda event: (setattr(self.__human, "nextMove", "W"), self.takeTurn()) if self.__human else None)
        window.bind("<s>", lambda event: (setattr(self.__human, "nextMove", "S"), self.takeTurn()) if self.__human else None)
        window.bind("<a>", lambda event: (setattr(self.__human, "nextMove", "A"), self.takeTurn()) if self.__human else None)
        window.bind("<d>", lambda event: (setattr(self.__human, "nextMove", "D"), self.takeTurn()) if self.__human else None)
        window.bind("<f>", lambda event: (setattr(self.__human, "abilityTimer", 5), self.updateGame()) if self.__human and self.__human.abilityTimer == -5 else None)

        self.center()

    def appendLog(self, message):
        self.__logs.config(state="normal")
        self.__logs.insert(tk.END, message + "\n")
        self.__logs.see(tk.END)
        self.__logs.config(state="disabled")

    def addOrganism(self, organism):
        addedHuman = False

        # Only one human can be present in the world
        if isinstance(organism, Human):
            if self.__human is None:
                self.__human = organism
                addedHuman = True
            else:
                return False


        if 0 <= organism.x < self.cols and 0 <= organism.y < self.rows:
            if isinstance(organism, Hogweed):
                self.hogweedMap[(organism.x, organism.y)] = True
            organism.world = self
            self.__order.append(organism)
            self.takenCells[(organism.x, organism.y)] = True
            self.appendLog(f"{organism}: Was created")
            return True
        else:
            if addedHuman:
                self.__human = None
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
            elif isinstance(organism, Human):
                self.__human = None

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

        self.appendLog(f"-- Turn {self.__turn} --")

        # Only organisms that are alive and created before the turn will take action
        for i in range(n):
            organism = self.__order[i]

            if organism.alive:
                organism.action()

        self.removeDead()
        self.updateGame()
        self.__turn += 1

    def run(self):
        self.updateGame()
        self.__window.mainloop()

    def save(self):
        with open("save.txt", "w") as file:
            file.write(f"{self.rows}\n")
            file.write(f"{self.cols}\n")
            file.write(f"{self.__turn}\n")
            file.write("---\n")

            for organism in self.__order:
                file.write(f"{organism.__class__.__name__};{organism.x};{organism.y};{organism.age};{organism.strength}\n")

            file.write("---\n")

            file.write(self.__logs.get("1.0", "end-1c"))

            if not self.human is None:
                file.write("---\n")
                file.write(f"{self.human.abilityTimer}")

    def load(self):
        with open("save.txt", "r") as file:
            self.__rows = int(file.readline().strip())
            self.__cols = int(file.readline().strip())
            self.__turn = int(file.readline().strip())

            self.__human = None
            self.__order = []
            self.takenCells = {}
            self.hogweedMap = {}

            for x in range(self.__cols):
                for y in range(self.__rows):
                    self.takenCells[(x, y)] = False
                    self.hogweedMap[(x, y)] = False

            file.readline() # ---

            for line in file:
                if line.strip() == "---":
                    break

                name, x, y, age, strength = line.split(";")
                x, y, age, strength = map(int, (x, y, age, strength))

                classes = {
                    "Antelope": Antelope,
                    "CyberSheep": CyberSheep,
                    "Fox": Fox,
                    "Human": Human,
                    "Sheep": Sheep,
                    "Turtle": Turtle,
                    "Wolf": Wolf,
                    "Dandelion": Dandelion,
                    "DeadlyNightshade": DeadlyNightshade,
                    "Grass": Grass,
                    "Guarana": Guarana,
                    "Hogweed": Hogweed,
                }

                organism = classes.get(name)

                if organism:
                    new_organism = organism(x, y)
                    new_organism.age = age
                    new_organism.strength = strength

                    self.addOrganism(new_organism)

            oldWindow = self.__window
            self.__window = tk.Tk()
            self.__gameGrid = None

            self.__logs = None

            self.initWindow()
            oldWindow.destroy()

            for line in file:
                if line.strip() == "---":
                    break

                self.appendLog(line.strip())

            if not self.human is None:
                self.human.abilityTimer = int(file.readline().strip())

            self.updateGame()