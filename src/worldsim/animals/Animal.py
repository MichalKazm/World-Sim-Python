import random
from abc import ABC
from typing import override

from worldsim.Organism import Organism


class Animal(Organism, ABC):
    def __init__(self, strength, initiative, x, y):
        super().__init__(strength, initiative, x, y)

    @override
    def collision(self, other):
        if type(self) == type(other):
            success = False

            if self.world.getOrganism(self.x, self.y - 1) is None:
                success = self.world.addOrganism(self.createNew(self.x, self.y - 1))

            if not success and self.world.getOrganism(self.x, self.y + 1) is None:
                success = self.world.addOrganism(self.createNew(self.x, self.y + 1))

            if not success and self.world.getOrganism(self.x - 1, self.y) is None:
                success = self.world.addOrganism(self.createNew(self.x - 1, self.y))

            if not success and self.world.getOrganism(self.x + 1, self.y) is None:
                success = self.world.addOrganism(self.createNew(self.x + 1, self.y))

            if not success and self.world.getOrganism(other.x, other.y - 1) is None:
                success = self.world.addOrganism(self.createNew(other.x, other.y - 1))

            if not success and self.world.getOrganism(other.x, other.y + 1) is None:
                success = self.world.addOrganism(self.createNew(other.x, other.y + 1))

            if not success and self.world.getOrganism(other.x - 1, other.y) is None:
                success = self.world.addOrganism(self.createNew(other.x - 1, other.y))

            if not success and self.world.getOrganism(other.x + 1, other.y) is None:
                success = self.world.addOrganism(self.createNew(other.x + 1, other.y))
        else:
            self.__x = other.x
            self.__y = other.y
            if self.strength >= other.strength:
                other.dies()
            else:
                self.dies()


    @override
    def action(self):
        newX = self.x
        newY = self.y

        # Count available directions
        available = 0

        if self.x > 0:
            available += 1

        if self.x < self.world.cols - 1:
            available += 1

        if self.y > 0:
            available += 1

        if self.y < self.world.rows - 1:
            available += 1

        # Move in a random available direction
        chosenMove = 4

        if available != 0:
            chosenMove = random.randint(0, chosenMove - 1)

        # Move up
        if self.y > 0:
            if chosenMove == 0:
                newY = self.y - 1

            chosenMove -= 1

        # Move down
        if self.y < self.world.rows - 1:
            if chosenMove == 0:
                newY = self.y + 1

            chosenMove -= 1

        # Move left
        if self.x > 0:
            if chosenMove == 0:
                newX = self.x - 1

            chosenMove -= 1

        # Move right
        if self.x < self.world.cols - 1:
            if chosenMove == 0:
                newX = self.x + 1

            chosenMove -= 1

        if chosenMove < 0:
            other = self.world.getOrganism(newX, newY)

            if other is None:
                self.__x = newX
                self.__y = newY
            else:
                self.collision(other)

        self.__age += 1