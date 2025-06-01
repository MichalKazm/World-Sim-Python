import random
from typing import override

from worldsim.Organism import Organism

class Plant(Organism):
    def __init__(self, strength, x, y, symbol, color):
        super().__init__(strength, 0, x, y, symbol, color)

    @override
    def collision(self, other):
        self.world.appendLog(f"{other}: Ate {self}")
        self.dies()

    @override
    def action(self):
        # 10% chance
        if random.randint(0, 9) == 0:
            available = 0
            newX = self.x
            newY = self.y

            if self.y > 0 and not self.world.takenCells[(self.x, self.y - 1)]:
                available += 1

            if self.y < self.world.rows - 1 and not self.world.takenCells[(self.x, self.y + 1)]:
                available += 1

            if self.x > 0 and not self.world.takenCells[(self.x - 1, self.y)]:
                available += 1

            if self.x < self.world.cols - 1 and not self.world.takenCells[(self.x + 1, self.y)]:
                available += 1

            # Create a new plant in a random empty adjacent cell
            chosenCell = 4

            if available != 0:
                chosenCell = random.randint(0, available - 1)

            # Cell above
            if self.y > 0 and not self.world.takenCells[(self.x, self.y - 1)]:
                if chosenCell == 0:
                    newY = self.y - 1
                    self.world.addOrganism(self.createNew(newX, newY))

                chosenCell -= 1

            # Cell below
            if self.y < self.world.rows - 1 and not self.world.takenCells[(self.x, self.y + 1)]:
                if chosenCell == 0:
                    newY = self.y + 1
                    self.world.addOrganism(self.createNew(newX, newY))

                chosenCell -= 1

            # Cell to the left
            if self.x > 0 and not self.world.takenCells[(self.x - 1, self.y)]:
                if chosenCell == 0:
                    newX = self.x - 1
                    self.world.addOrganism(self.createNew(newX, newY))

                chosenCell -= 1

            # Cell to the right
            if self.x < self.world.cols - 1 and not self.world.takenCells[(self.x + 1, self.y)]:
                if chosenCell == 0:
                    newX = self.x + 1
                    self.world.addOrganism(self.createNew(newX, newY))

                chosenCell -= 1

            if chosenCell < 0:
                self.world.appendLog(f"{self}: Spread to ({newX}, {newY})")

        self.age += 1