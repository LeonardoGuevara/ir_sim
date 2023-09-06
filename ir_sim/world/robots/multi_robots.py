from ir_sim.world import MultiObjects
import numpy as np

class MultiRobots(MultiObjects):
    def __init__(self, type=None, number=0, **kwargs) -> None:

        robot_class = RobotFactory[type]
        
        super().__init__(robot_class, number, role='robot', **kwargs)

        pass





    