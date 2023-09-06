from math import inf
import numpy as np
from ir_sim.global_param import world_param 


class BehaviorFactory:
    pass



class Behavior:
    def __init__(self, object_info=None, behavior='dash') -> None:

        self.behavior = behavior
        self.object_info = object_info    
    
    def GenVel(self, state, goal, velocity, behavior_name='dash', **behavior_kwargs):

        functionality = BehaviorFactory[self.object_info.dynamics][behavior_name]

        min_vel = np.maximum(self.vel_min, velocity - self.object_info.acce * world_param.step_time)
        max_vel = np.minimum(self.vel_max, velocity + self.object_info.acce * world_param.step_time)

        behavior_vel = functionality(state, goal, velocity, min_vel, max_vel, **behavior_kwargs)

        return behavior_vel

    def cal_dash_vel(self, state, goal, velocity):
        pass
        
        