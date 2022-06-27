import logging
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from pynput import keyboard
from multiprocessing import Process
from .env_robot import EnvRobot
from .env_obstacle import EnvObstacle
from ir_sim2.world import RobotDiff, RobotAcker, RobotOmni, ObstacleCircle, ObstaclePolygon
from ir_sim2.log.Logger import Logger

class EnvBase:

    robot_factory={'robot_diff': RobotDiff, 'robot_acker': RobotAcker, 'robot_omni': RobotOmni}
    obstacle_factory = {'obstacle_circle': ObstacleCircle, 'obstacle_polygon': ObstaclePolygon}

    def __init__(self, world_name=None, plot=True, logging=True, control_mode='auto', **kwargs):
        
        # world_name: path of the yaml
        # plot: True or False
        # control_mode: auto, keyboard

        world_args, robot_args, obstacle_args = dict(), dict(), dict() 

        if world_name != None:
            world_name = sys.path[0] + '/' + world_name

            with open(world_name) as file:
                com_list = yaml.load(file, Loader=yaml.FullLoader)
                world_args = com_list.get('world', dict())
                robot_args = com_list.get('robots', dict())
                obstacle_args_list = com_list.get('obstacles', [])

        world_args.update(kwargs.get('world_args', dict()))
        robot_args.update(kwargs.get('robot_args', dict()))
        [obstacle_args.update(kwargs.get('obstacle_args', dict())) for obstacle_args in obstacle_args_list]

        # world args
        self.__height = world_args.get('world_height', 10)
        self.__width = world_args.get('world_width', 10) 
        self.step_time = world_args.get('step_time', 0.01) 
        self.sample_time = world_args.get('sample_time', 0.1)
        self.offset_x = world_args.get('offset_x', 0) 
        self.offset_y = world_args.get('offset_y', 0)

        self.robot_args = robot_args
        self.obstacle_args_list = obstacle_args_list

        self.plot = plot
        self.components = dict()
        self.init_environment(**kwargs)

        self.log = Logger('robot.log', level='info')
        self.logging = logging

        self.count = 0
        self.sampling = True
        self.arrive_flag = False
        self.collision_flag = False

        if control_mode == 'keyboard':
            pass

    def init_environment(self, **kwargs):
        # full=False, keep_path=False, 
        # kwargs: full: False,  full windows plot
        #         keep_path, keep a residual
        #         robot kwargs:
        #         obstacle kwargs:
        self.env_robot = EnvRobot(self.robot_factory[self.robot_args['type']], step_time=self.step_time, **self.robot_args)
        self.env_obstacle_list = [EnvObstacle(self.obstacle_factory[oa['type']], step_time=self.step_time, **oa) for oa in self.obstacle_args_list]
       
        # default robots 
        self.robot_list = self.env_robot.robot_list
        self.robot = self.robot_list[0] if len(self.robot_list) > 0 else None
        
        # default obstacles
        # plot
        if self.plot:
            self.fig, self.ax = plt.subplots()
            self.init_plot(self.ax, **kwargs)
            # self.fig, self.ax = plt.subplots()
        
        # self.components['env_robot_list'] = self.env_robot_list
        self.components['env_robot'] = self.env_robot

    def cal_des_vel(self, **kwargs):
        return self.env_robot.cal_des_vel(**kwargs)
         
    def robots_step(self, vel_list, **kwargs):
        self.env_robot.move(vel_list, **kwargs)

    def obstacles_step(self, **kwargs):
        [ env_obs.move() for env_obs in self.env_obstacle_list if env_obs.dynamic]

    def step(self, vel_list=[], **kwargs):
        self.robots_step(vel_list, **kwargs)
        self.obstacles_step(**kwargs)
        self.count += 1
        self.sampling = (self.count % (self.sample_time / self.step_time) == 0)


    def step_count(self, **kwargs):
        self.count += 1
        self.sampling = (self.count % (self.sample_time / self.step_time) == 0)

    def collision_check(self):
        return any([self.env_robot.collision_check(env_obstacle) for env_obstacle in self.env_obstacle_list])

    def done(self, collision_check=True):
        
        if self.env_robot.arrive():
            self.arrive_flag = True
            if self.logging: self.log.logger.info('All robots arrive at the goal positions')
        if collision_check and self.collision_check():
            self.collision_flag = True
            if self.logging: self.log.logger.warning('Collisions occur')

        return self.arrive_flag or self.collision_flag
    
    def done_list(self):
        return self.env_robot.arrive_list()

    def render(self, pause_time=0.0001, **kwargs):
        
        if self.plot and self.sampling:
            self.draw_components(self.ax, mode='dynamic', **kwargs)
            plt.pause(pause_time)
            self.clear_components(self.ax, mode='dynamic', **kwargs)
    
    def render_once(self, pause_time=0.0001, **kwargs):
        if self.plot:
            self.draw_components(self.ax, mode='dynamic', **kwargs)
            plt.pause(pause_time)
            self.clear_components(self.ax, mode='dynamic', **kwargs)
            
    def init_plot(self, ax, **kwargs):
        ax.set_aspect('equal')
        ax.set_xlim(self.offset_x, self.offset_x + self.__width)
        ax.set_ylim(self.offset_y, self.offset_y + self.__height)
        
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")

        self.draw_components(ax, mode='static', **kwargs)
    
    def draw_components(self, ax, mode='all', **kwargs):
        # mode: static, dynamic, all
        if mode == 'static':
            [env_obs.plot(ax, **kwargs) for env_obs in self.env_obstacle_list if not env_obs.dynamic]
        elif mode == 'dynamic':
            self.env_robot.plot(ax, **kwargs)
            [env_obs.plot(ax, **kwargs) for env_obs in self.env_obstacle_list if env_obs.dynamic]

        elif mode == 'all':
            self.env_robot.plot(ax, **kwargs)
            [env_obs.plot(ax, **kwargs) for env_obs in self.env_obstacle_list]
            # obstacle
        else:
            self.logger.error('error input of the draw mode')

    def clear_components(self, ax, mode='all', **kwargs):
        if mode == 'dynamic':
            self.env_robot.plot_clear(ax)
            [env_obs.plot_clear() for env_obs in self.env_obstacle_list if env_obs.dynamic]

        elif mode == 'static':
            pass
        
        elif mode == 'all':
            plt.cla()
        

    def show(self, **kwargs):
        if self.plot:
            self.draw_components(self.ax, mode='dynamic', **kwargs)
            plt.show()

    def reset(self):
        self.env_robot.reset()
        [env_obs.reset() for env_obs in self.env_obstacle_list if env_obs.dynamic]


            



    


            