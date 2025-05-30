from abc import ABC, abstractmethod

from worldsim.world.World import World


class Organism(ABC):
    def __init__(self, strength, initiative, y, x):
        self.__strength = strength
        self.__initiative = initiative
        self.__y = y
        self.__x = x
        self.__age = 0
        self.__alive = True
        self.__world = None

    @property
    def strength(self):
        return self.__strength

    @property
    def initiative(self):
        return self.__initiative

    @property
    def y(self):
        return self.__y

    @property
    def x(self):
        return self.__x

    @property
    def age(self):
        return self.__age

    @property
    def alive(self):
        return self.__alive

    @property
    def world(self):
        return self.__world

    @world.setter
    def world(self, world):
        if isinstance(world, World):
            self.__world = world

    def dies(self):
        self.__alive = False

    @abstractmethod
    def createNew(self, y, x):
        pass

    @abstractmethod
    def collision(self, other):
        pass

    @abstractmethod
    def action(self):
        pass