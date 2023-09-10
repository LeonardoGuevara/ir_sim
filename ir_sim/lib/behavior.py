from math import inf
import numpy as np
from ir_sim.global_param import world_param
from ir_sim.util.util import relative_position, WrapToPi


class BehaviorDiff:
    def __init__(self, object_info=None, behavior_dict=None) -> None:

        self.object_info = object_info
        self.behavior_dict = behavior_dict

    def gen_behavior_vel(self, state, goal, min_vel, max_vel):
        
        if self.behavior_dict['name'] == 'dash':
            
            angle_tolerance = self.behavior_dict.get('angle_tolerance', 0.1)
            goal_threshold = self.object_info.goal_threshold

            distance, radian = relative_position(state, goal) 

            if distance < goal_threshold:
                return np.zeros((2, 1))


            diff_radian = WrapToPi( radian - state[2, 0] )

            linear = max_vel[0, 0] * np.cos(diff_radian)

            if abs(diff_radian) < angle_tolerance:
                angular = 0
            else:
                angular = max_vel[1, 0] * np.sign(diff_radian)

            return np.array([[linear], [angular]])
        









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

        self.behavior_dict = behavior_dict


    
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
        
        self.behavior_dynamics = Behavior_factory[object_info.dynamics](object_info, behavior_dict)

    def gen_vel(self, state, goal, min_vel, max_vel):
        return self.behavior_dynamics.gen_behavior_vel(state, goal, min_vel, max_vel)







        
        