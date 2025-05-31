import random
from abc import ABC
from typing import override

from worldsim.Organism import Organism


class Animal(Organism, ABC):
    def __init__(self, strength, initiative, x, y, symbol, color):
        super().__init__(strength, initiative, x, y, symbol, color)

    @override
    def collision(self, other):
        # If two organisms are of the same type, they reproduce
        if type(self) == type(other):
            success = False

            if 0 <= self.x < self.world.cols and 0 <= self.y - 1 < self.world.rows:
                if not self.world.takenCells[(self.x, self.y - 1)]:
                    success = self.world.addOrganism(self.createNew(self.x, self.y - 1))

            if not success:
                if 0 <= self.x < self.world.cols and 0 <= self.y + 1 < self.world.rows:
                    if not self.world.takenCells[(self.x, self.y + 1)]:
                        success = self.world.addOrganism(self.createNew(self.x, self.y + 1))

            if not success:
                if 0 <= self.x - 1 < self.world.cols and 0 <= self.y < self.world.rows:
                    if not self.world.takenCells[(self.x - 1, self.y)]:
                        success = self.world.addOrganism(self.createNew(self.x - 1, self.y))

            if not success:
                if 0 <= self.x + 1 < self.world.cols and 0 <= self.y < self.world.rows:
                    if not self.world.takenCells[(self.x + 1, self.y)]:
                        success = self.world.addOrganism(self.createNew(self.x + 1, self.y))

            if not success:
                if 0 <= other.x < self.world.cols and 0 <= other.y - 1 < self.world.rows:
                    if not self.world.takenCells[(other.x, other.y - 1)]:
                        success = self.world.addOrganism(self.createNew(other.x, other.y - 1))

            if not success:
                if 0 <= other.x < self.world.cols and 0 <= other.y + 1 < self.world.rows:
                    if not self.world.takenCells[(other.x, other.y + 1)]:
                        success = self.world.addOrganism(self.createNew(other.x, other.y + 1))

            if not success:
                if 0 <= other.x - 1 < self.world.cols and 0 <= other.y < self.world.rows:
                    if not self.world.takenCells[(other.x - 1, other.y)]:
                        success = self.world.addOrganism(self.createNew(other.x - 1, other.y))

            if not success:
                if 0 <= other.x + 1 < self.world.cols and 0 <= other.y < self.world.rows:
                    if not self.world.takenCells[(other.x + 1, other.y)]:
                        success = self.world.addOrganism(self.createNew(other.x + 1, other.y))

            if success:
                self.world.appendLog(f"{self}: Reproduced with {other}")
        else:
            self.world.appendLog(f"{self}: Attacked {other}")

            self.world.takenCells[(self.x, self.y)] = False
            self.x = other.x
            self.y = other.y
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
            chosenMove = random.randint(0, available - 1)

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
                self.world.appendLog(f"{self}: Moved to ({newX}, {newY})")

                self.world.takenCells[(self.x, self.y)] = False
                self.x = newX
                self.y = newY
                self.world.takenCells[(newX, newY)] = True
            else:
                self.collision(other)

        self.age += 1