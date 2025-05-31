from typing import override

from worldsim.animals.Animal import Animal

class Wolf(Animal):
    def __init__(self, x, y):
        super().__init__(9, 5, x, y, "W", "gray45")

    @override
    def createNew(self, x, y):
        return Wolf(x, y)