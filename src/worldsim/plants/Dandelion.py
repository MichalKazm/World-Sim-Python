from typing import override

from worldsim.plants.Plant import Plant


class Dandelion(Plant):
    def __init__(self, x, y):
        super().__init__(0, x, y, "D", "yellow2")

    @override
    def createNew(self, x, y):
        return Dandelion(x, y)

    @override
    def action(self):
        for _ in range(3):
            super().action()

        # Age is incremented 3 times in loop
        self.age = self.age - 2