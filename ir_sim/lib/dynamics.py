import numpy as np
from math import cos, sin
from ir_sim.util.util import WrapToPi

def differential_wheel_dynamics(state, velocity, step_time, noise=False, alpha = [0.03, 0, 0, 0.03, 0, 0]):

    '''
    The dynamics function for differential wheel robot

    state: [x, y, theta]   (3*1) vector
    velocity: [linear, angular]  (2*1) vector
    '''

    assert state.shape == (3, 1) and velocity.shape==(2, 1)

    if noise:
        std_linear = np.sqrt(alpha[0] * (velocity[0, 0] ** 2) + alpha[1] * (velocity[1, 0] ** 2))
        std_angular = np.sqrt(alpha[2] * (velocity[0, 0] ** 2) + alpha[3] * (velocity[1, 0] ** 2))
        # gamma = alpha[4] * (velocity[0, 0] ** 2) + alpha[5] * (velocity[1, 0] ** 2)
        real_velocity = velocity + np.random.normal([[0], [0]], scale = [[std_linear], [std_angular]])  

    else:
        real_velocity = velocity

    coefficient_vel = np.zeros((3, 2))
    coefficient_vel[0, 0] = cos(state[2, 0])
    coefficient_vel[1, 0] = sin(state[2, 0])
    coefficient_vel[2, 1] = 1

    next_state = state + coefficient_vel @ real_velocity * step_time

    next_state[2, 0] = WrapToPi(next_state[2, 0])

    return next_state





    
        







    



# def motion_diff(cls, current_state, vel, step_time, noise = False, alpha = [0.03, 0, 0, 0.03, 0, 0]):
    
#     assert current_state.shape == cls.state_dim and vel.shape == cls.vel_dim and cls.robot_type == 'diff'

#     if noise:
#         std_linear = np.sqrt(alpha[0] * (vel[0, 0] ** 2) + alpha[1] * (vel[1, 0] ** 2))
#         std_angular = np.sqrt(alpha[2] * (vel[0, 0] ** 2) + alpha[3] * (vel[1, 0] ** 2))
#         # gamma = alpha[4] * (vel[0, 0] ** 2) + alpha[5] * (vel[1, 0] ** 2)
#         real_vel = vel + np.random.normal([[0], [0]], scale = [[std_linear], [std_angular]])
#     else:
#         real_vel = vel

#     coefficient_vel = np.zeros((3, 2))
#     coefficient_vel[0, 0] = cos(current_state[2, 0])
#     coefficient_vel[1, 0] = sin(current_state[2, 0])
#     coefficient_vel[2, 1] = 1

#     next_state = current_state + coefficient_vel @ real_vel * step_time

#     next_state[2, 0] = WrapToPi(next_state[2, 0])

#     return next_state