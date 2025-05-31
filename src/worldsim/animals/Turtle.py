import random
from typing import override

from worldsim.animals.Animal import Animal

class Turtle(Animal):
    def __init__(self, x, y):
        super().__init__(2, 1, x, y, "T", "green2")

    @override
    def didDeflectAttack(self, attacker):
        if attacker.strength < 5:
            self.world.appendLog(f"{self}: Pushed {attacker} back")
            return True
        else:
            return False

    @override
    def createNew(self, x, y):
        return Turtle(x, y)

    @override
    def action(self):
        # 25% chance
        if random.randint(0, 3) == 0:
            super().action()