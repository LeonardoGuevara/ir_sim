import numpy as np
from shapely import MultiPolygon, Point, Polygon, LineString, minimum_bounding_radius
import itertools
from typing import Optional
from ir_sim.lib.factory import dynamics_factory
from math import inf, pi
from dataclasses import dataclass
from ir_sim.global_param import world_param 
import logging
from ir_sim.util.util import WrapToRegion

@dataclass
class ObjectInfo:
    id: int
    shape: str
    dynamics: str
    role: str
    color: str
    static: bool
    goal: np.ndarray
    vel_min: np.ndarray
    vel_max: np.ndarray
    acce: np.ndarray
    angle_range: np.ndarray


class ObjectBase:

    id_iter = itertools.count()

    vel_dim = (2, 1)

    def __init__(self, shape: str='circle', shape_tuple=None, state=[0, 0, 0], velocity=[0, 0], goal=[0, 0, 0], dynamics: str='omni', role: str='obstacle', color='k', static=False, vel_min=[-inf, inf], vel_max=[-inf, inf], acce=[-inf, inf], angle_range=[-pi, pi], behavior=None, goal_threshold=0.1) -> None:

        '''
        parameters:
        -----------
            shape: the shape of the object, a string, including: circle, polygon, linestring,

            shape_tuple: tuple to init the geometry, default is None; A sequence of (x, y) numeric coordinate pairs or triples, or an array-like with shape (N, 2)
                for circle, the list should have be: (center_x, center_y, radius)
                for polygon, the list should have the element of vertices: [vertices], number of vertices >= 3
                for lineString, composed of one or more line segments, the list should have the element of vertices: [vertices]. 

            state: the state of the object, list or numpy. default is [0, 0, 0], [x, y, theta]
            velocity: the velocity of the object, list or numpy. default is [0, 0], [vx, vy]
            dynamics: the moving dynamics of the object, including omni, diff, acker, custom; default omni, if custom, 

            static: whether static object; default False

            role: the role of the object, including: robot, obstacle, landmark, target, default is 'obstacle'

            flag: 
                stop_flag: whether the object is stopped, default False
                arrive_flag: whether the object is arrived, default False
                collision_flag: whether the object is collided, default False

            behavior: the behavior of the object, 
                dash: the object will dash to the target position, and stop when arrive the target position
                wander: the object will wander in the world (random select goal to move)
                default is dash

        '''

        self._id = next(ObjectBase.id_iter)
        self._shape = shape
        self._geometry = self.construct_geometry(shape, shape_tuple)

        self._state = np.c_[state]
        self._velocity = np.c_[velocity]
        self._goal = np.c_[goal]

        self.dynamics = dynamics
        self._dynamics = dynamics_factory(dynamics)

        # flag
        self.stop_flag = False
        self.arrive_flag = False
        self.collision_flag = False

        # information
        self.info = ObjectInfo(self._id, shape, dynamics, role, color, static, np.c_[vel_min], np.c_[vel_max], np.c_[acce], np.c_[angle_range], self._goal)

        # arrive judgement
        self.goal_threshold = goal_threshold

        # sensor
        self.sensor = None

        # behavior
        self.behavior = behavior

        # plot 
        self.plot_patch_list = []
        self.plot_line_list = []
        self.plot_text_list = []

    def __repr__(self) -> str:
        pass

    def __eq__(self, o: object) -> bool:
        return self._id == o._id


    def step(self, velocity, **kwargs):

        if self.static or self.stop_flag:

            self._velocity = np.zeros_like(velocity)

            return self._state  

        else: 
            
            self.pre_process()

            behavior_vel = self.vel_with_behavior(velocity)

            new_state = self._dynamics(self._state, behavior_vel, **kwargs)
            next_state = self.mid_process(new_state)

            self._state = next_state
            self._velocity = behavior_vel


            self.sensor_step()
            self.post_process()
            self.check_arrive()
                
            return next_state

    def vel_with_behavior(self, velocity, custom_behavior=None):

        if isinstance(vel, list): vel = np.c_[vel]
        if velocity.ndim == 1: vel = vel[:, np.newaxis]

        assert velocity.shape == self.vel_dim
 
        input_kwargs = {'state': self._state, 'goal': self._goal, 'min_vel': min_vel, 'max_vel': max_vel}

        if self.behavior is None:
            behavior_vel = velocity

        elif self.behavior == 'dash':
            behavior_vel = self.dash(velocity, min_vel, max_vel)

        elif self.behavior == 'wander':
            behavior_vel = self.wander(velocity, min_vel, max_vel)
        
        elif self.behavior == 'custom':
            behavior_vel = custom_behavior(velocity, min_vel, max_vel)

        else:
            print("behavior is not defined, use the input velocity")
            behavior_vel = velocity

        if (behavior_vel < min_vel).any():
            logging.warning("velocity is smaller than min_vel, velocity is clipped to min_vel")
        elif (behavior_vel > max_vel).any():
            logging.warning("velocity is larger than max_vel, velocity is clipped to max_vel")

        behavior_vel_clip = np.clip(behavior_vel, min_vel, max_vel)


        return behavior_vel_clip


    def custor_behavior(self, velocity, min_vel, max_vel):
        pass






    def vel_check(self, velocity):
        
        if isinstance(vel, list): vel = np.c_[vel]
        if velocity.ndim == 1: vel = vel[:, np.newaxis]

        assert velocity.shape == self.vel_dim
 
        min_vel = np.maximum(self.vel_min, self._velocity - self.acce * world_param.step_time)
        max_vel = np.minimum(self.vel_max, self._velocity + self.acce * world_param.step_time)

        if (velocity < min_vel).any():
            logging.warning("velocity is smaller than min_vel, velocity is clipped to min_vel")
        elif (velocity > max_vel).any():
            logging.warning("velocity is larger than max_vel, velocity is clipped to max_vel")

        velocity_clip = np.clip(velocity, min_vel, max_vel)

        return velocity_clip

    def pre_process(self):
        # collision check
        pass
        

    def post_process(self):
        pass
    
    def mid_process(self, state):
        state[2, 0] = WrapToRegion(state[2, 0], self.info.angle_range)

        return state


    def construct_geometry(self, shape, shape_tuple):

        if shape == 'circle':
            geometry = Point([ shape_tuple[0], shape_tuple[1] ]).buffer(shape_tuple[2])

        elif shape == 'polygon':
            geometry = Polygon(shape_tuple)

        elif shape == 'linestring':
            geometry = LineString(shape_tuple)

        else:
            raise ValueError("shape should be one of the following: circle, polygon, linestring")

        return geometry


    def geometry_state_transition(self):
        pass
    

    # get information

    def get_inequality_Ab(self, s):
        # general inequality Ax <= b 
        
        if self.shape == 'circle':
            pass
            

        elif self.shape == 'polygon':
            pass

        elif self.shape == 'linestring':
            pass
        
    
        return A, b


    def set_state(self, state):

        if isinstance(state, list): state = np.c_[state]

        state[2, 0] = WrapToRegion(state[2, 0], self.info.angle_range)

        self._state = state
    

    # get information
    def get_info(self):
        return self.info

    # property
    @property
    def name(self):
        return self.info.role + '_' + str(self.id)

    @property
    def shape(self):
        return self._shape

    @property
    def geometry(self):
        return self._geometry

    @property
    def centroid(self):
        return self._geometry.centroid
        
    @property
    def id(self):
        return self._id
    
    @property
    def state(self):
        return self._state
    
    @property
    def position(self):
        # return the position of the object
        return self._state[:2]

    @property
    def radius(self):

        '''
        return the minimum bounding radius
        '''
    
        return minimum_bounding_radius(self._geometry)
    
    @property
    def arrive(self):
        return self.arrive_flag

    @property
    def ineq_Ab(self):
        return self.get_inequality_Ab()






    # Operators

