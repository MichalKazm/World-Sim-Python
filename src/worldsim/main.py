from worldsim.display.World import World
from worldsim.animals.Wolf import Wolf
from worldsim.animals.Sheep import Sheep
from worldsim.animals.Fox import Fox
from worldsim.animals.Turtle import Turtle
from worldsim.animals.Antelope import Antelope
from worldsim.plants.Grass import Grass
from worldsim.plants.Dandelion import Dandelion
from worldsim.plants.Guarana import Guarana
from worldsim.plants.DeadlyNightshade import DeadlyNightshade
from worldsim.plants.Hogweed import Hogweed

world = World(40,20)

world.addOrganism(Wolf(2, 2))
world.addOrganism(Wolf(2, 3))
world.addOrganism(Sheep(19, 19))
world.addOrganism(Sheep(20, 19))
world.addOrganism(Sheep(18, 19))
world.addOrganism(Fox(10, 10))
world.addOrganism(Turtle(5, 5))
world.addOrganism(Antelope(30, 19))
world.addOrganism(Grass(39, 0))
world.addOrganism(Dandelion(39 , 10))
world.addOrganism(Guarana(25, 5))
world.addOrganism(DeadlyNightshade(39, 5))
world.addOrganism(Hogweed(5, 15))

world.run()

print("Hello World!")