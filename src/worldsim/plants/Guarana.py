from typing import override

from worldsim.plants.Plant import Plant


class Guarana(Plant):
    def __init__(self, x, y):
        super().__init__(0, x, y, "*", "red3")

    @override
    def createNew(self, x, y):
        return Guarana(x, y)

    @override
    def collision(self, other):
        self.world.appendLog(f"{other}: Ate {self}")

        newStrength = other.strength + 3

        self.world.appendLog(f"{other}: Strength increased from {other.strength} to {newStrength}")

        other.strength = newStrength

        self.dies()