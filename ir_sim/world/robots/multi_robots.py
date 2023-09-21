import numpy as np
from ir_sim.util.util import extend_list
from ir_sim.world.multi_object_base import MultiObjects
from ir_sim.world.robots.robot_factory import RobotFactory

class MultiRobots(MultiObjects):
    def __init__(self, number, distribution, **kwargs) -> None:

        dynamics = kwargs.pop('dynamics', None)

        super().__init__(dynamics, number, distribution, role='robot', **kwargs)


        self.number = number
        self.dynamics = dynamics

        temp = RobotFactory()

        # self.robot_list = [ temp.create_robot(dynamics, shape, state=state, behavior=behavior, **kwargs) for state, shape, behavior in zip(self.state_list, self.shape_list, self.behavior_list) ]

        dynamics_name = dynamics.pop('name', 'omni')


        if self.behavior_list is None:
            self.robot_list = [ temp.create_robot(dynamics_name, dynamics, shape, state=state, **kwargs) for state, shape in zip(self.state_list, self.shape_list) ]

        else:
            self.robot_list = [ temp.create_robot(dynamics_name, dynamics, shape, state=state, behavior=behavior, **kwargs) for state, shape, behavior in zip(self.state_list, self.shape_list, self.behavior_list) ]

        



        
        
        
    





    