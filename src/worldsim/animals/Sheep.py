from typing import override

from worldsim.animals.Animal import Animal

class Sheep(Animal):
    def __init__(self, x, y):
        super().__init__(4, 4, x, y, "S", "light pink")

    @override
    def createNew(self, x, y):
        return Sheep(x, y)