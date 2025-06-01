from typing import override

from worldsim.plants.Plant import Plant


class DeadlyNightshade(Plant):
    def __init__(self, x, y):
        super().__init__(99, x, y, "N", "dark slate gray")

    @override
    def createNew(self, x, y):
        return DeadlyNightshade(x, y)

    @override
    def collision(self, other):
        self.world.appendLog(f"{other}: Ate {self}")

        if self.strength <= other.strength:
            self.dies()

        other.dies()