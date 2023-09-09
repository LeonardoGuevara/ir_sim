from math import inf
import numpy as np
from ir_sim.global_param import world_param 


class BehaviorDiff:
    def __init__(self, object_info=None, behavior_dict=None) -> None:

        self.object_info = object_info
        self.behavior_dict = behavior_dict

    def gen_behavior_vel(self, state, goal, min_vel, max_vel):
        
        vel = np.zeros((2, 1))


    # def cal_des_vel(self, tolerance=0.12):
    #     # calculate desire velocity
    #     des_vel = np.zeros((2, 1))

    #     if self.arrive_mode == 'position':

    #         dis, radian = RobotDiff.relative_position(self.state, self.goal)      

    #         if dis < self.goal_threshold:
    #             return des_vel
    #         else:
    #             diff_radian = RobotDiff.wraptopi( radian - self.state[2, 0] )
    #             des_vel[0, 0] = np.clip(self.vel_acce_max[0, 0] * cos(diff_radian), 0, inf) 

    #             if abs(diff_radian) < tolerance:
    #                 des_vel[1, 0] = 0
    #             else:
    #                 des_vel[1, 0] = self.vel_acce_max[1, 0] * (diff_radian / abs(diff_radian))

    #     elif self.arrive_mode == 'state':
    #         pass
        
    #     return des_vel


class BehaviorAcker:
    def __init__(self, object_info=None, behavior_dict=None) -> None:
        super().__init__(object_info, behavior_dict)
    
    def gen_behavior_vel(state, goal, min_vel, max_vel, **kwargs):
        pass

class BehaviorOmni:
    def __init__(self) -> None:
        pass
    
    def gen_behavior_vel(state, goal, min_vel, max_vel, **kwargs):
        pass

Behavior_factory = {'diff': BehaviorDiff, 'acker': BehaviorAcker, 'omni': BehaviorOmni}

class Behavior:
    def __init__(self, object_info=None, behavior_dict=None) -> None:
        self.object_info = object_info
        self.behavior_dict = behavior_dict

        self.behavior_dynamics = Behavior_factory[object_info.dynamics]

    def gen_vel(self, state, goal, min_vel, max_vel, **kwargs):
        return self.behavior_dynamics.gen_behavior_vel(state, goal, min_vel, max_vel, **kwargs)




        
        