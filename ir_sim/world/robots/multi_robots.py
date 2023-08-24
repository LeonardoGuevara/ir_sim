from ir_sim.world import MultiObjects
import numpy as np

class MultiRobots(MultiObjects):
    def __init__(self, robot_class=None, number=0, **kwargs) -> None:
        super().__init__(robot_class, number, role='robot', **kwargs)

        pass





    