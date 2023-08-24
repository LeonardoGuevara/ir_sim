from ir_sim.world import MultiObjects
import numpy as np

class MultiObstacles(MultiObjects):
    def __init__(self, obstacle_class=None, number=0, **kwargs) -> None:
        super().__init__(obstacle_class, number, role='obstacle', **kwargs)

        pass





    