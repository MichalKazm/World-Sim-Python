from typing import override

from worldsim.plants.Plant import Plant

class Grass(Plant):
    def __init__(self, x, y):
        super().__init__(0, x, y, "G", "forest green")

    @override
    def createNew(self, x, y):
        return Grass(x, y)