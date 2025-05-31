from abc import ABC, abstractmethod

class Organism(ABC):
    def __init__(self, strength, initiative, x, y, symbol, color):
        self.__strength = strength
        self.__initiative = initiative
        self.__x = x
        self.__y = y
        self.__age = 0
        self.__symbol = symbol
        self.__color = color
        self.__alive = True
        self.__world = None

    @property
    def strength(self):
        return self.__strength

    @property
    def initiative(self):
        return self.__initiative

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, newX):
        self.__x = newX

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, newY):
        self.__y = newY

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, newAge):
        self.__age = newAge

    @property
    def symbol(self):
        return self.__symbol

    @property
    def color(self):
        return self.__color

    @property
    def alive(self):
        return self.__alive

    @property
    def world(self):
        return self.__world

    @world.setter
    def world(self, newWorld):
        self.__world = newWorld

    def dies(self):
        self.world.appendLog(f"{self}: Died")
        self.__alive = False

    @abstractmethod
    def createNew(self, x, y):
        pass

    @abstractmethod
    def collision(self, other):
        pass

    @abstractmethod
    def action(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__} ({self.x}, {self.y})"