from worldsim.display.World import World
from worldsim.animals.Wolf import Wolf
from worldsim.animals.Sheep import Sheep
from worldsim.animals.Fox import Fox
from worldsim.animals.Turtle import Turtle

world = World(55,35)

world.addOrganism(Wolf(2, 2))
world.addOrganism(Wolf(2, 3))
world.addOrganism(Sheep(19, 20))
world.addOrganism(Sheep(20, 20))
world.addOrganism(Sheep(20, 21))
world.addOrganism(Fox(10, 10))
world.addOrganism(Turtle(5, 5))

world.run()

print("Hello World!")