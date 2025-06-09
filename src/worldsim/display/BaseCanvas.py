import tkinter as tk
from abc import abstractmethod, ABC

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


class BaseCanvas(tk.Canvas, ABC):
    def __init__(self, world, parent, cols, rows, width, height, cellSize):
        super().__init__(parent, width=width, height=height, bg="black", highlightthickness=0)

        self.__world = world
        self.__cols = cols
        self.__rows = rows
        self.__cellSize = cellSize
        self.__cells = {}
        self.__menu = None
        self.__clickedCol = None
        self.__clickedRow = None

        self.initGrid()
        self.initPopup()

    @property
    def world(self):
        return self.__world

    @property
    def cols(self):
        return self.__cols

    @property
    def rows(self):
        return self.__rows

    @property
    def cellSize(self):
        return self.__cellSize

    @property
    def cells(self):
        return self.__cells

    @property
    def menu(self):
        return self.__menu

    @menu.setter
    def menu(self, newMenu):
        self.__menu = newMenu

    @property
    def clickedCol(self):
        return self.__clickedCol

    @clickedCol.setter
    def clickedCol(self, newClickedCol):
        self.__clickedCol = newClickedCol

    @property
    def clickedRow(self):
        return self.__clickedRow

    @clickedRow.setter
    def clickedRow(self, newClickedRow):
        self.__clickedRow = newClickedRow

    @abstractmethod
    def initGrid(self):
        pass

    @abstractmethod
    def showPopup(self, event):
        pass

    def initPopup(self):
        world = self.__world
        menu = tk.Menu(self, tearoff=0)
        self.menu = menu

        menu.add_command(label="Antelope",
                         command=lambda : (world.addOrganism(Antelope(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="CyberSheep",
                         command=lambda : (world.addOrganism(CyberSheep(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="Fox",
                         command=lambda : (world.addOrganism(Fox(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="Human",
                         command=lambda : (world.addOrganism(Human(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="Sheep",
                         command=lambda : (world.addOrganism(Sheep(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="Turtle",
                         command=lambda: (world.addOrganism(Turtle(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="Wolf",
                         command=lambda : (world.addOrganism(Wolf(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="Dandelion",
                         command=lambda : (world.addOrganism(Dandelion(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="DeadlyNightshade",
                         command=lambda : (world.addOrganism(DeadlyNightshade(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="Grass",
                         command=lambda : (world.addOrganism(Grass(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="Guarana",
                         command=lambda : (world.addOrganism(Guarana(self.clickedCol, self.clickedRow)), world.updateGame()))
        menu.add_command(label="Hogweed",
                         command=lambda : (world.addOrganism(Hogweed(self.clickedCol, self.clickedRow)), world.updateGame()))

        self.bind("<Button-1>", self.showPopup)

    def clear(self):
        for polygon, label in self.cells.values():
            self.itemconfig(polygon, fill="white")
            self.itemconfig(label, text="")

    def draw(self, order):
        for organism in order:
            if organism.alive:
                polygon, label = self.cells[(organism.x, organism.y)]

                self.itemconfig(polygon, fill=organism.color)
                if isinstance(organism, Human) and organism.abilityTimer > 0:
                    self.itemconfig(polygon, fill=organism.abilityColor)

                self.itemconfig(label, text=organism.symbol)