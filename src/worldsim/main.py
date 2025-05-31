from worldsim.display.World import World
from worldsim.animals.Wolf import Wolf

world = World(55,35)

world.addOrganism(Wolf(2, 2))
world.addOrganism(Wolf(2, 3))
world.addOrganism(Wolf(3, 2))

world.run()

print("Hello World!")