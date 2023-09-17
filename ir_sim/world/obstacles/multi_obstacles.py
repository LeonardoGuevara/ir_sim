import numpy as np
from ir_sim.util.util import extend_list
from ir_sim.world.multi_object_base import MultiObjects
from ir_sim.world.obstacles.obstacle_factory import ObstacleFactory

class MultiObstacles(MultiObjects):
    def __init__(self, number, distribution, **kwargs) -> None:

        dynamics = kwargs.pop('dynamics', None)

        super().__init__(dynamics, number, distribution, role='robot', **kwargs)


        self.number = number
        self.dynamics = dynamics

        temp = ObstacleFactory()


        if self.behavior_list is None:

            self.obstacle_list = [ temp.create_obstacle(dynamics, shape, state=state, **kwargs) for state, shape in zip(self.state_list, self.shape_list) ]

        else:
            self.obstacle_list = [ temp.create_obstacle(dynamics, shape, state=state, behavior=behavior, **kwargs) for state, shape, behavior in zip(self.state_list, self.shape_list, self.behavior_list) ]

        


    
        



        
        
        
    





    