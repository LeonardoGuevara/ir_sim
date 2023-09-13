import numpy as np
from shapely import MultiPolygon, Point, Polygon, LineString, minimum_bounding_radius
import itertools
from typing import Optional
from ir_sim.lib.factory import dynamics_factory
from math import inf, pi, atan2, cos, sin, sqrt
from dataclasses import dataclass
from ir_sim.global_param import world_param 
import logging
from ir_sim.util.util import WrapToRegion, get_transform
from ir_sim.lib.behavior import Behavior
import matplotlib as mpl
from shapely.ops import transform




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
    goal_threshold: float


    def add_property(self, key, value):
        setattr(self, key, value)



class ObjectBase:

    id_iter = itertools.count()
    vel_dim = (2, 1)

    def __init__(self, shape: str='circle', shape_tuple=None, state=[0, 0, 0], velocity=[0, 0], goal=[10, 10, 0], dynamics: str='omni', role: str='obstacle', color='k', static=False, vel_min=[-1, -1], vel_max=[1, 1], acce=[inf, inf], angle_range=[-pi, pi], behavior=None, goal_threshold=0.1, **kwargs) -> None:

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
        self._init_geometry = self.construct_geometry(shape, shape_tuple)

        self._state = np.c_[state]
        self._velocity = np.c_[velocity]
        self._goal = np.c_[goal]

        self.dynamics = dynamics
    
        # flag
        self.stop_flag = False
        self.arrive_flag = False
        self.collision_flag = False

        # information
        self.static = static
        self.vel_min = np.c_[vel_min]
        self.vel_max = np.c_[vel_max]
        self.info = ObjectInfo(self._id, shape, dynamics, role, color, static, np.c_[goal], np.c_[vel_min], np.c_[vel_max], np.c_[acce], np.c_[angle_range], goal_threshold)

        # arrive judgement
        self.goal_threshold = goal_threshold

        # sensor
        self.sensor = None

        # behavior
        self.obj_behavior = Behavior(self.info, behavior)

        # plot 
        self.plot_patch_list = []
        self.plot_line_list = []
        self.plot_text_list = []

    def __repr__(self) -> str:
        pass

    def __eq__(self, o: object) -> bool:
        return self._id == o._id


    def step(self, velocity=None, **kwargs):

        if self.static or self.stop_flag:

            self._velocity = np.zeros_like(velocity)

            return self._state  

        else: 
            
            self.pre_process()

            behavior_vel = self.gen_behavior_vel(velocity)

            new_state = self._dynamics(behavior_vel, **kwargs)
            next_state = self.mid_process(new_state)

            self._state = next_state
            self._velocity = behavior_vel

            self._geometry = self.geometry_transform(self._init_geometry, self._state)

            self.sensor_step()
            self.post_process()
            self.check_status()
                
            return next_state


    def sensor_step(self):
        pass
    

    def _dynamics(self, velocity, **kwargs):
        # default is omni
        new_state = self._state + velocity * world_param.step_time

        return new_state

    def geometry_transform(self, geometry, state):

        def transfor_with_state(x, y):

            trans, rot = get_transform(state)

            # point = np.array([[x], [y]])
            points = np.array([x, y])

            new_points = rot @ points + trans

            return (new_points[0, :], new_points[1, :])
        
        new_geometry = transform(transfor_with_state, geometry)

        return new_geometry

        
    
    # check arrive
    def check_status(self):
        
        self.check_arrive()
        self.check_collision()

        if world_param.collision_mode == 'stop':
            self.stop_flag = self.collision_flag
        


    def check_arrive(self):

        if np.linalg.norm(self._state[:2] - self._goal[:2]) < self.goal_threshold:
            self.arrive_flag = True
        else:
            self.arrive_flag = False

        

    def check_collision(self):
        pass
        

    def gen_behavior_vel(self, velocity):

        min_vel, max_vel = self.get_vel_range()
        
        if velocity is None:
            
            if self.obj_behavior is None:
                print("Error: behavior and input velocity is not defined")

            else:
                behavior_vel = self.obj_behavior.gen_vel(self._state, self._goal, min_vel, max_vel)
            
        else:
            if isinstance(vel, list): vel = np.c_[vel]
            if velocity.ndim == 1: vel = vel[:, np.newaxis]

            assert velocity.shape == self.vel_dim

            behavior_vel = velocity

        # input_kwargs = {'state': self._state, 'goal': self._goal, 'min_vel': min_vel, 'max_vel': max_vel}

        if (behavior_vel < min_vel).any():
            logging.warning("velocity is smaller than min_vel, velocity is clipped to min_vel")
        elif (behavior_vel > max_vel).any():
            logging.warning("velocity is larger than max_vel, velocity is clipped to max_vel")

        behavior_vel_clip = np.clip(behavior_vel, min_vel, max_vel)


        return behavior_vel_clip



    def custom_behavior(self, velocity, min_vel, max_vel):
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
    
    
    def plot(self, ax, show_goal=False, show_text=False, show_arrow=False, show_uncertainty=False, show_trajectory=False, show_trail=False, **kwargs):

        # object_color = 'g', goal_color='r', show_goal=True, show_text=False, show_traj=False, traj_type='-g', fontsize=10, 

        self.plot_object(ax, **kwargs)

        if show_goal:
            self.plot_goal(ax, **kwargs)

        if show_text:
            self.plot_text(ax, **kwargs)

        if show_arrow:
            self.plot_arrow(ax, **kwargs)

        if show_uncertainty:
            self.plot_uncertainty(ax, **kwargs)

        if show_trajectory:
            self.plot_trajectory(ax, **kwargs)
        
        if show_trail:
            self.plot_trail(ax, **kwargs)

        
    def plot_object(self, ax, obj_color='g', **kwargs):

        x = self.state[0, 0]
        y = self.state[1, 0]

        if self.shape == 'circle':

            object_patch = mpl.patches.Circle(xy=(x, y), radius = self.radius, color = obj_color)
            object_patch.set_zorder(3)

        elif self.shape == 'polygon':
            pass
        

        ax.add_patch(object_patch)
        self.plot_patch_list.append(object_patch)


    def plot_trajectory(self, ax, **kwargs):
        pass 

    def plot_goal(self, ax, goal_color='r', **kwargs):

        goal_x = self._goal[0, 0]
        goal_y = self._goal[1, 0]
        
        goal_circle = mpl.patches.Circle(xy=(goal_x, goal_y), radius=self.radius, color=goal_color, alpha=0.5)
        goal_circle.set_zorder(1)
    
        ax.add_patch(goal_circle)

        self.plot_patch_list.append(goal_circle)


    def plot_text(self, ax, **kwargs):
        pass

    def plot_arrow(self, ax, arrow_length=0.4, arrow_width=0.6, **kwargs):

        x = self._state[0][0]
        y = self._state[1][0]
        theta = self._state[2][0]

        arrow = mpl.patches.Arrow(x, y, arrow_length*cos(theta), arrow_length*sin(theta), width=arrow_width)
        arrow.set_zorder(3)
        ax.add_patch(arrow)
        
        self.plot_patch_list.append(arrow)

    def plot_trail(self, ax, **kwargs):
        pass

    
    # if show_trail:
    #         if trail_type == 'rectangle':
    #             car_rect = mpl.patches.Rectangle(xy=(start_x, start_y), width=self.shape[0], height=self.shape[1], angle=r_phi_ang, edgecolor=self.edgecolor, fill=False, alpha=0.8, linewidth=0.8)
    #             ax.add_patch(car_rect)

    #         elif trail_type == 'circle':
    #             x = (min(self.vertex[0, :]) + max(self.vertex[0, :])) / 2
    #             y = (min(self.vertex[1, :]) + max(self.vertex[1, :])) / 2

    #             car_circle = mpl.patches.Circle(xy=(x, y), radius = self.shape[0] / 2, edgecolor='red', fill=False)
    #             ax.add_patch(car_circle)






    def plot_uncertainty(self, ax, **kwargs):
        pass

    def plot_clear(self):
        
        [patch.remove() for patch in self.plot_patch_list]
        [line.pop(0).remove() for line in self.plot_line_list]
        [text.remove() for text in self.plot_text_list]

        self.plot_patch_list = []
        self.plot_line_list = []
        self.plot_text_list = []


    def done(self):

        if self.stop_flag or self.arrive_flag or self.collision_flag:
            return True
        else:
            return False

        
        


        














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

    def get_vel_range(self):

        min_vel = np.maximum(self.vel_min, self._velocity - self.info.acce * world_param.step_time)
        max_vel = np.minimum(self.vel_max, self._velocity + self.info.acce * world_param.step_time)

        return min_vel, max_vel



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
    
    @property
    def vertices(self):
        return self._geometry.exterior.coords._coords.T






    # Operators

