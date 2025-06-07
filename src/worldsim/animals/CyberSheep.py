from typing import override

from worldsim.animals.Animal import Animal
from worldsim.plants.Plant import Plant


class CyberSheep(Animal):
    def __init__(self, x, y):
        super().__init__(10, 4, x, y, "#", "RoyalBlue2")

    @override
    def createNew(self, x, y):
        return CyberSheep(x, y)

    @override
    def action(self):
        newX = self.x
        newY = self.y

        distance = None
        for otherY in range(self.world.rows):
            for otherX in range(self.world.cols):
                if self.world.hogweedMap[(otherX, otherY)]:
                    newDistance = abs(self.x - otherX) + abs(self.y - otherY)
                    if distance is None or newDistance < distance:
                        distance = newDistance
                        closestX = otherX
                        closestY = otherY

        if not distance is None:
            if closestY < self.y:
                # Move up
                newY = self.y - 1
            elif closestX > self.x:
                # Move right
                newX = self.x + 1
            elif closestY > self.y:
                # Move down
                newY = self.y + 1
            elif closestX < self.x:
                # Move left
                newX = self.x - 1

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
        else:
            # If didn't find a hogweed move like a normal sheep (basic Animal movement)
            super().action()