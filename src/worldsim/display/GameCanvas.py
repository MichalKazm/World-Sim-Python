import tkinter as tk

from worldsim.animals.Antelope import Antelope
from worldsim.animals.CyberSheep import CyberSheep
from worldsim.animals.Fox import Fox
from worldsim.animals.Human import Human
from worldsim.animals.Sheep import Sheep
from worldsim.animals.Turtle import Turtle
from worldsim.animals.Wolf import Wolf
from worldsim.plants.Dandelion import Dandelion
from worldsim.plants.DeadlyNightshade import DeadlyNightshade
from worldsim.plants.Grass import Grass
from worldsim.plants.Guarana import Guarana
from worldsim.plants.Hogweed import Hogweed


class GameCanvas(tk.Canvas):
    def __init__(self, world, parent, cols, rows, cell_size=30):
        height = rows * cell_size
        width = cols * cell_size
        super().__init__(parent, width=width + 4, height=height + 4, bg="black", highlightthickness=0)

        self.__world = world
        self.__cols = cols
        self.__rows = rows
        self.__cell_size = cell_size
        self.__cells = {}
        self.__menu = None
        self.__clickedCol = None
        self.__clickedRow = None

        self.initGrid()
        self.initPopup()

    def initGrid(self):
        for y in range(self.__rows):
            for x in range(self.__cols):
                x1 = x * self.__cell_size
                y1 = y * self.__cell_size
                x2 = x1 + self.__cell_size
                y2 = y1 + self.__cell_size

                rect = self.create_rectangle(x1, y1, x2, y2, fill="white")
                label = self.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="", font=("Arial", 12, "bold"))

                self.__cells[(x, y)] = (rect, label)

    def showPopup(self, event):
        self.__clickedCol = event.x // self.__cell_size
        self.__clickedRow = event.y // self.__cell_size

        # Check if cell is occupied
        if not self.__world.takenCells[self.__clickedCol, self.__clickedRow]:
            self.__menu.tk_popup(event.x_root, event.y_root)

        # Check if Human exists
        if self.__world.human is None:
            self.__menu.entryconfig(3, state="normal")
        else:
            self.__menu.entryconfig(3, state="disabled")

    def initPopup(self):
        world = self.__world
        menu = tk.Menu(self, tearoff=0)
        self.__menu = menu

        menu.add_command(label="Antelope",
                         command=lambda : (world.addOrganism(Antelope(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="CyberSheep",
                         command=lambda : (world.addOrganism(CyberSheep(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="Fox",
                         command=lambda : (world.addOrganism(Fox(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="Human",
                         command=lambda : (world.addOrganism(Human(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="Sheep",
                         command=lambda : (world.addOrganism(Sheep(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="Turtle",
                         command=lambda: (world.addOrganism(Turtle(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="Wolf",
                         command=lambda : (world.addOrganism(Wolf(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="Dandelion",
                         command=lambda : (world.addOrganism(Dandelion(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="DeadlyNightshade",
                         command=lambda : (world.addOrganism(DeadlyNightshade(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="Grass",
                         command=lambda : (world.addOrganism(Grass(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="Guarana",
                         command=lambda : (world.addOrganism(Guarana(self.__clickedCol, self.__clickedRow)), world.updateGame()))
        menu.add_command(label="Hogweed",
                         command=lambda : (world.addOrganism(Hogweed(self.__clickedCol, self.__clickedRow)), world.updateGame()))

        self.bind("<Button-1>", self.showPopup)

    def clear(self):
        for rect, label in self.__cells.values():
            self.itemconfig(rect, fill="white")
            self.itemconfig(label, text="")

    def draw(self, order):
        for organism in order:
            if organism.alive:
                rect, label = self.__cells[(organism.x, organism.y)]

                self.itemconfig(rect, fill=organism.color)
                if isinstance(organism, Human) and organism.abilityTimer > 0:
                    self.itemconfig(rect, fill=organism.abilityColor)

                self.itemconfig(label, text=organism.symbol)