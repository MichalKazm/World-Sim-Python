import random
from typing import override

from worldsim.animals.Animal import Animal
from worldsim.animals.Antelope import Antelope
from worldsim.plants.Plant import Plant


class Human(Animal):
    def __init__(self, x, y):
        super().__init__(5, 4, x, y, "@", "MediumOrchid1")
        self.__nextMove = " "
        self.__abilityTimer = -5
        self.__abilityColor = "DarkOrchid3"

    @property
    def nextMove(self):
        return self.__nextMove

    @nextMove.setter
    def nextMove(self, newNextMove):
        self.__nextMove = newNextMove

    @property
    def abilityTimer(self):
        return self.__abilityTimer

    @abilityTimer.setter
    def abilityTimer(self, newAbilityTimer):
        self.__abilityTimer = newAbilityTimer

    @property
    def abilityColor(self):
        return self.__abilityColor

    @override
    def createNew(self, x, y):
        return None

    @override
    def collision(self, other):
        self.world.appendLog(f"{self}: Attacked {other}")

        if isinstance(other, Antelope):
            self.world.takenCells[(self.x, self.y)] = False
            self.x = other.x
            self.y = other.y
        if not other.didDeflectAttack(self):
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

        moved = False
        doubleMove = False

        # First 3 turns when ability is active
        if self.abilityTimer > 2:
            doubleMove = True
        elif self.abilityTimer > 0:
            # Last 2 turns when ability is active
            if random.randint(0, 1) == 0:
                doubleMove = True

        if doubleMove:
            if self.world.gridType == "square":
                match self.nextMove:
                    case "W":
                        if self.y > 1:
                            newY = self.y -2
                            moved = True
                    case "S":
                        if self.y < self.world.rows - 2:
                            newY = self.y + 2
                            moved = True
                    case "A":
                        if self.x > 1:
                            newX = self.x - 2
                            moved = True
                    case "D":
                        if self.x < self.world.cols - 2:
                            newX = self.x + 2
                            moved = True
            else:
                match self.nextMove:
                    case "Q":
                        if self.x > 1 and self.y > 1:
                            newX = self.x - 2
                            newY = self.y - 1
                            moved = True
                    case "W":
                        if self.y > 1:
                            newY = self.y - 2
                            moved = True
                    case "E":
                        if self.x < self.world.cols - 2 and self.y > 1:
                            newX = self.x + 2
                            newY = self.y - 1
                            moved = True
                    case "A":
                        if self.x > 1 and self.y < self.world.rows - 2:
                            newX = self.x - 2
                            newY = self.y + 1
                            moved = True
                    case "S":
                        if self.y < self.world.rows - 2:
                            newY = self.y + 2
                            moved = True
                    case "D":
                        if self.x < self.world.cols - 2 and self.y < self.world.rows - 2:
                            newX = self.x + 2
                            newY = self.y + 1
                            moved = True
        else:
            if self.world.gridType == "square":
                match self.nextMove:
                    case "W":
                        if self.y > 0:
                            newY = self.y - 1
                            moved = True
                    case "S":
                        if self.y < self.world.rows - 1:
                            newY = self.y + 1
                            moved = True
                    case "A":
                        if self.x > 0:
                            newX = self.x - 1
                            moved = True
                    case "D":
                        if self.x < self.world.cols - 1:
                            newX = self.x + 1
                            moved = True
            else:
                match self.nextMove:
                    case "Q":
                        if self.x % 2 == 0:
                            if self.x > 0 and self.y > 0:
                                newX = self.x - 1
                                newY = self.y - 1
                                moved = True
                        else:
                            if self.x > 0:
                                newX = self.x - 1
                                moved = True
                    case "W":
                        if self.y > 0:
                            newY = self.y - 1
                            moved = True
                    case "E":
                        if self.x % 2 == 0:
                            if self.x < self.world.cols - 1 and self.y > 0:
                                newX = self.x + 1
                                newY = self.y - 1
                                moved = True
                        else:
                            if self.x < self.world.cols - 1:
                                newX = self.x + 1
                                moved = True
                    case "A":
                        if self.x % 2 == 0:
                            if self.x > 0:
                                newX = self.x - 1
                                moved = True
                        else:
                            if self.x > 0 and self.y < self.world.rows - 1:
                                newX = self.x - 1
                                newY = self.y + 1
                                moved = True
                    case "S":
                            if self.y < self.world.rows - 1:
                                newY = self.y + 1
                                moved = True
                    case "D":
                            if self.x % 2 == 0:
                                if self.x < self.world.cols - 1:
                                    newX = self.x + 1
                                    moved = True
                            else:
                                if self.x < self.world.cols - 1 and self.y < self.world.rows - 1:
                                    newX = self.x + 1
                                    newY = self.y + 1
                                    moved = True

        if moved:
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

        if self.abilityTimer > -5:
            self.abilityTimer -= 1

        self.age += 1