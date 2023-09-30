from ir_sim.world import ObjectBase
import numpy as np
from math import cos, sin, pi
from ir_sim.util.util import WrapToPi
from ir_sim.global_param import world_param 


class RobotDiff(ObjectBase):
    def __init__(self, shape='circle', shape_tuple=None, color='g', **kwargs):
        super(RobotDiff, self).__init__(shape=shape, shape_tuple=shape_tuple, dynamics='diff', role='robot', color=color, **kwargs)


    def _dynamics(self, velocity, mode='diff', noise=False, alpha=[0.03, 0, 0, 0.03, 0, 0],  **kwargs):
        
        # def differential_wheel_dynamics(state, velocity, step_time, noise=False, alpha = [0.03, 0, 0, 0.03, 0, 0]):

        '''
        The dynamics function for differential wheel robot

        state: [x, y, theta]   (3*1) vector
        velocity: [linear, angular]  (2*1) vector
        mode: 'diff', 'omni', 'wheel', 
        '''
        
        assert velocity.shape==(2, 1)
        assert self._state.shape==(3, 1)

        if mode == 'diff':
            pass
        elif mode == 'omni':
            pass
        elif mode == 'wheel':
            pass


        if noise:
            std_linear = np.sqrt(alpha[0] * (velocity[0, 0] ** 2) + alpha[1] * (velocity[1, 0] ** 2))
            std_angular = np.sqrt(alpha[2] * (velocity[0, 0] ** 2) + alpha[3] * (velocity[1, 0] ** 2))
            # gamma = alpha[4] * (velocity[0, 0] ** 2) + alpha[5] * (velocity[1, 0] ** 2)
            real_velocity = velocity + np.random.normal([[0], [0]], scale = [[std_linear], [std_angular]])  

        else:
            real_velocity = velocity

        coefficient_vel = np.zeros((3, 2))
        coefficient_vel[0, 0] = cos(self._state[2, 0])
        coefficient_vel[1, 0] = sin(self._state[2, 0])
        coefficient_vel[2, 1] = 1

        next_state = self._state + coefficient_vel @ real_velocity * world_param.step_time

        next_state[2, 0] = WrapToPi(next_state[2, 0])

        return next_state


    def plot(self, ax, show_goal=True, show_arrow=True, **kwargs):
        super().plot(ax, show_goal=show_goal, show_arrow = show_arrow, **kwargs)


    






        








