from abc import ABC, abstractmethod

class Organism(ABC):
    def __init__(self, strength: int, initiative: int, y: int, x: int):
        self.__strength = strength
        self.__initiative = initiative
        self.__y = y
        self.__x = x
        self.__age = 0
        self.__alive = True

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

    @abstractmethod
    def collision(self, other: 'Organism'):
        pass

    @abstractmethod
    def action(self):
        pass