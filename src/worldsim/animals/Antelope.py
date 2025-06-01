import random
from typing import override

from worldsim.animals.Animal import Animal
from worldsim.plants.Plant import Plant


class Antelope(Animal):
    def __init__(self, x, y):
        super().__init__(4, 4, x, y, "A", "dark goldenrod")

    @override
    def didDeflectAttack(self, attacker):
        # 50% chance
        if random.randint(0, 1) == 0:
            newX = self.x
            newY = self.y

            success = False
            if self.y > 0:
                if not self.world.takenCells[(self.x, self.y - 1)]:
                    newY = self.y - 1
                    success = True
            if not success:
                if self.y < self.world.rows - 1:
                    if not self.world.takenCells[(self.x, self.y + 1)]:
                        newY = self.y + 1
                        success = True

            if not success:
                if self.x > 0:
                    if not self.world.takenCells[(self.x - 1, self.y)]:
                        newX = self.x - 1
                        success = True

            if not success:
                if self.x < self.world.cols - 1:
                    if not self.world.takenCells[(self.x + 1, self.y)]:
                        newX = self.x + 1
                        success = True

            if success:
                self.world.takenCells[(self.x, self.y)] = False
                self.world.appendLog(f"{self}: Fled to ({newX}, {newY})")
                self.world.appendLog(f"{attacker}: Moved to ({self.x}, {self.y})")
                self.y = newY
                self.x = newX
                self.world.takenCells[(newX, newY)] = True
                return True

        return False

    @override
    def createNew(self, x, y):
        return Antelope(x, y)

    @override
    def action(self):
        newX = self.x
        newY = self.y

        # Count available directions
        available = 0

        if self.x > 1:
            available += 1

        if self.x < self.world.cols - 2:
            available += 1

        if self.y > 1:
            available += 1

        if self.y < self.world.rows - 2:
            available += 1

        # Move in a random available direction
        chosenMove = 4

        if available != 0:
            chosenMove = random.randint(0, available - 1)

        # Move up
        if self.y > 1:
            if chosenMove == 0:
                newY = self.y - 2

            chosenMove -= 1

        # Move down
        if self.y < self.world.rows - 2:
            if chosenMove == 0:
                newY = self.y + 2

            chosenMove -= 1

        # Move left
        if self.x > 1:
            if chosenMove == 0:
                newX = self.x - 2

            chosenMove -= 1

        # Move right
        if self.x < self.world.cols - 2:
            if chosenMove == 0:
                newX = self.x + 2

            chosenMove -= 1

        if chosenMove < 0:
            other = self.world.getOrganism(newX, newY)

            if other is None:
                self.world.appendLog(f"{self}: Moved to ({newX}, {newY})")

                self.world.takenCells[(self.x, self.y)] = False
                self.x = newX
                self.y = newY
                self.world.takenCells[(newX, newY)] = True
            else:
                if isinstance(other, Plant):
                    self.world.takenCells[(self.x, self.y)] = False
                    self.x = newX
                    self.y = newY
                    self.world.appendLog(f"{self}: Moved to ({newX}, {newY})")
                    other.collision(self)
                else:
                    self.collision(other)

        self.age += 1