from worldsim.Organism import Organism


class World:
    def __init__(self, rows: int, cols: int):
        self.__rows = rows
        self.__cols = cols
        self.__order = []

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    def addOrganism(self, organism):
        if 0 <= organism.y < self.rows and 0 <= organism.x < self.cols:
            self.__order.append(organism)

    def sortOrder(self):
        self.__order.sort(key=lambda organism : (organism.initiative, organism.age), reverse=True)
