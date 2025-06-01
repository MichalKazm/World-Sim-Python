import random
from typing import override

from worldsim.animals.Animal import Animal
from worldsim.plants.Plant import Plant


class Fox(Animal):
    def __init__(self, x, y):
        super().__init__(3, 7, x, y, "F", "orange")

    @override
    def createNew(self, x, y):
        return Fox(x, y)

    @override
    def action(self):
        newX = self.x
        newY = self.y

        # Count available directions
        available = 0

        if self.x > 0:
            other = self.world.getOrganism(self.x , self.y - 1)
            if other is None or self.strength >= other.strength:
                available += 1

        if self.x < self.world.cols - 1:
            other = self.world.getOrganism(self.x, self.y + 1)
            if other is None or self.strength >= other.strength:
                available += 1

        if self.y > 0:
            other = self.world.getOrganism(self.x - 1, self.y)
            if other is None or self.strength >= other.strength:
                available += 1

        if self.y < self.world.rows - 1:
            other = self.world.getOrganism(self.x + 1, self.y)
            if other is None or self.strength >= other.strength:
                available += 1

        # Move in a random available direction
        chosenMove = 4

        if available != 0:
            chosenMove = random.randint(0, available - 1)

        # Move up
        if self.y > 0:
            other = self.world.getOrganism(self.x, self.y - 1)

            if other is None or self.strength >= other.strength:
                if chosenMove == 0:
                    newY = self.y - 1

                chosenMove -= 1


        # Move down
        if self.y < self.world.rows - 1:
            other = self.world.getOrganism(self.x, self.y + 1)

            if other is None or self.strength >= other.strength:
                if chosenMove == 0:
                    newY = self.y + 1

                chosenMove -= 1


        # Move left
        if self.x > 0:
            other = self.world.getOrganism(self.x - 1, self.y)

            if other is None or self.strength >= other.strength:
                if chosenMove == 0:
                    newX = self.x - 1

                chosenMove -= 1


        # Move right
        if self.x < self.world.cols - 1:
            other = self.world.getOrganism(self.x + 1, self.y)

            if other is None or self.strength >= other.strength:
                if chosenMove == 0:
                    newX = self.x + 1

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