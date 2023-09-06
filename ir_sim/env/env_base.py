import yaml

from ir_sim.util.util import file_check
from ir_sim.world import world, MultiRobots, MultiObstacles
from .env_plot import EnvPlot
import threading
from ir_sim.global_param import world_param
import time
import sys

class EnvBase:

    '''
    The base class of environment.

        parameters:
            world_name: the name of the world file, default is None
    
    
    '''

    def __init__(self, world_name=None, **kwargs):

        world_file_path = file_check(world_name)
        
        world_kwargs, plot_kwargs, robot_kwargs_list, robots_kwargs_list, obstacle_kwargs_list, obstacles_kwargs  = dict(), dict(), [], [], [], []

        if world_file_path != None:
           
            with open(world_file_path) as file:
                com_list = yaml.load(file, Loader=yaml.FullLoader)
                world_kwargs = com_list.get('world', dict())
                plot_kwargs = com_list.get('plot', dict())
                robot_kwargs_list = com_list.get('robot', list())
                robots_kwargs_list = com_list.get('robots', list())
                obstacle_kwargs_list = com_list.get('obstacle', list())
                obstacles_kwargs_list = com_list.get('obstacles', list())

        # for python 3.10
        # world_kwargs |= kwargs.get('world', dict())
        # plot_kwargs |= kwargs.get('plot', dict())
        # robots_kwargs |= kwargs.get('robots', dict())
        # obstacles_kwargs |= kwargs.get('obstacles', dict())
        # robot_kwargs |= kwargs.get('robot', dict())

        world_kwargs.update(kwargs.get('world', dict()))
        plot_kwargs.update(kwargs.get('plot', dict()))

        [robot_kw.update(kw) for (robot_kw, kw) in zip( robot_kwargs_list, kwargs.get('robot', list()) )]
        [robots_kw.update(kw) for (robots_kw, kw) in zip( robots_kwargs_list, kwargs.get('robots', list()) )]
        [obstacle_kw.update(kw) for (obstacle_kw, kw) in zip( obstacle_kwargs_list, kwargs.get('obstacle', list()) )]
        [obstacles_kw.update(kw) for (obstacles_kw, kw) in zip( obstacles_kwargs_list, kwargs.get('obstacles', list()) )]

        # init world, robot, obstacles
        self.world = world(**world_kwargs)

        self.robot_list = [ Robot(**robot_kw) for robot_kw in robot_kwargs_list]
        self.robots_list = [ MultiRobots(**robots_kwargs) for robots_kwargs in robots_kwargs_list ]
        self.obstacle_list = [ Obstacle(**obstacle_kw) for obstacle_kw in obstacle_kwargs_list]
        self.obstacles_list = [ MultiRobots(**obstacles_kw) for obstacles_kw in obstacles_kwargs_list ]
        
        self.objects = self.robot_list + self.robots_list + self.obstacle_list + self.obstacles_list     
        self.env_plot = EnvPlot(self.world.grid_map, self.objects, self.world.x_range, self.world.y_range, **plot_kwargs)

        # set env param


        # # thread
        # self.step_thread = threading.Thread(target=self.step)
    
    # def start(self, duration=500, **kwargs):

    #     self.step_thread.start()

    #     while world_param.count < duration:
    #         print(world_param.count)
    #         self.render(world_param.step_time)


    def start(self, duration=500):
        pass
        
    def step(self, action=None, **kwargs):

        self.objects_step()
        self.world.step()

    def render(self, interval=0.05):
        pass


    def show(self):
        self.env_plot.show()

    def end(self):
        print('end')
        

    


