from typing import override

from worldsim.animals.Animal import Animal
from worldsim.plants.Plant import Plant


class Hogweed(Plant):
    def __init__(self, x, y):
        super().__init__(10, x, y, "H", "ivory2")

    @override
    def createNew(self, x, y):
        return Hogweed(x, y)

    @override
    def collision(self, other):
        self.world.appendLog(f"{other}: Ate {self}")

        if self.strength <= other.strength:
            self.dies()

        other.dies()

    @override
    def action(self):
        # Kill animals adjacent to this plant
        killed = 0

        # Cell above
        other = self.world.getOrganism(self.x, self.y - 1)
        if isinstance(other, Animal):
            self.world.takenCells[(other.x, other.y)] = False
            other.dies()
            killed += 1
        # Cell below
        other = self.world.getOrganism(self.x, self.y + 1)
        if isinstance(other, Animal):
            self.world.takenCells[(other.x, other.y)] = False
            other.dies()
            killed += 1
        # Cell to the left
        other = self.world.getOrganism(self.x - 1, self.y)
        if isinstance(other, Animal):
            self.world.takenCells[(other.x, other.y)] = False
            other.dies()
            killed += 1
        # Cell to the right
        other = self.world.getOrganism(self.x + 1, self.y)
        if isinstance(other, Animal):
            self.world.takenCells[(other.x, other.y)] = False
            other.dies()
            killed += 1

        if killed > 0:
            self.world.appendLog(f"{self}: Killed {killed} animals adjacent to it")

        super().action()