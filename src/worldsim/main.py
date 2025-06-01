from worldsim.display.World import World
from worldsim.animals.Wolf import Wolf
from worldsim.animals.Sheep import Sheep
from worldsim.animals.Fox import Fox
from worldsim.animals.Turtle import Turtle
from worldsim.animals.Antelope import Antelope
from worldsim.plants.Grass import Grass
from worldsim.plants.Dandelion import Dandelion
from worldsim.plants.Guarana import Guarana

world = World(50,30)

world.addOrganism(Wolf(2, 2))
world.addOrganism(Wolf(2, 3))
world.addOrganism(Sheep(19, 20))
world.addOrganism(Sheep(20, 20))
world.addOrganism(Sheep(20, 21))
world.addOrganism(Fox(10, 10))
world.addOrganism(Turtle(5, 5))
world.addOrganism(Antelope(30, 25))
world.addOrganism(Grass(40, 0))
world.addOrganism(Dandelion(40 , 25))
world.addOrganism(Guarana(25, 5))

world.run()

print("Hello World!")