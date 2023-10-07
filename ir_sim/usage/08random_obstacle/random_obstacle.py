from ir_sim.env import EnvBase

env = EnvBase('random_obstacle.yaml')

for i in range(300):

    env.step()
    env.render(0.05)
    
    if env.done():
        break


env.end(10)
