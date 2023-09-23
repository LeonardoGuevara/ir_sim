import yaml

from ir_sim.util.util import file_check
# from ir_sim.world import world, MultiRobots, MultiObstacles
from ir_sim.world import world
from .env_plot import EnvPlot
import threading
from ir_sim.global_param import world_param, env_param
import time
import sys
from ir_sim.world.robots.robot_factory import RobotFactory
from ir_sim.world.obstacles.obstacle_factory import ObstacleFactory
from matplotlib import pyplot as plt
from ir_sim.world.robots.multi_robots import MultiRobots
from ir_sim.world.obstacles.multi_obstacles import MultiObstacles



class EnvBase:

    '''
    The base class of environment.

        parameters:
            world_name: the name of the world file, default is None
    
    
    '''

    def __init__(self, world_name=None, display=True, disable_all_plot=False, save_ani=False, **kwargs):

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

        robot_factory = RobotFactory() 
        obstacle_factory = ObstacleFactory() 

        self.robot_list = [ robot_factory.create_robot_single(**robot_kw) for robot_kw in robot_kwargs_list]
        self.robots_list = [ MultiRobots(**robots_kwargs) for robots_kwargs in robots_kwargs_list ]
        self.obstacle_list = [ obstacle_factory.create_obstacle_single(**obstacle_kw) for obstacle_kw in obstacle_kwargs_list]
        self.obstacles_list = [ MultiObstacles(**obstacles_kw) for obstacles_kw in obstacles_kwargs_list ]
        
        # self.objects = self.robot_list + self.robots_list + self.obstacle_list + self.obstacles_list 
        
        robots_sum_list = [robot for robots in self.robots_list for robot in robots.robot_list]
        obstacles_sum_list = [obstacle for obstacles in self.obstacles_list for obstacle in obstacles.obstacle_list]

        self.objects = self.robot_list + robots_sum_list + self.obstacle_list + obstacles_sum_list
        

        self.env_plot = EnvPlot(self.world.grid_map, self.objects, self.world.x_range, self.world.y_range, **plot_kwargs)

        # set env param
        self.display = display
        self.disable_all_plot = disable_all_plot

        self.save_ani = save_ani

        env_param.objects = self.objects

        # # thread
        # self.step_thread = threading.Thread(target=self.step)
    
    # def start(self, duration=500, **kwargs):

    #     self.step_thread.start()

    #     while world_param.count < duration:
    #         print(world_param.count)
    #         self.render(world_param.step_time)

    def __del__(self):
        print('Simulated Environment End')

    def start(self, duration=500):
        pass
    
    # step
    def step(self, action=None, **kwargs):
        self.objects_step(action)
        self.world.step()

    def objects_step(self, action=None):
        [ obj.step(action) for obj in self.objects]


        
    def render(self, interval=0.05, **kwargs):

        # figure_args: arguments when saving the figures for animation, see https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html for detail
        # default figure arguments

        if not self.disable_all_plot: 
            if self.world.sampling:

                if self.display: plt.pause(interval)

                if self.save_ani: self.env_plot.save_gif_figure(**kwargs)

                self.env_plot.clear_components('dynamic', self.objects, **kwargs)
                self.env_plot.draw_components('dynamic', self.objects, **kwargs)
                

    def show(self):
        self.env_plot.show()


    def draw_trajectory(self, traj, traj_type='g-', **kwargs):
        self.env_plot.draw_trajectory(traj, traj_type, **kwargs)



    def end(self, ending_time=1, **kwargs):

        if self.save_ani:
            self.env_plot.save_animate(**kwargs)


        print(f'Figure will be closed within {ending_time:d} seconds.')
        plt.pause(ending_time)
        plt.close()
        

    def done(self, mode='all'):

        done_list = [ obj.done() for obj in self.objects if obj.role=='robot']

        if len(done_list) == 0:
            return False

        if mode == 'all':
            return all(done_list)
        elif mode == 'any':
            return any(done_list)
        
    def reset(self):
        self.reset_all() 

    def reset_all(self):
        [obj.reset() for obj in self.objects]
        

    #     def reset(self, mode='now', **kwargs):
    #     # mode: 
    #     #   default: reset the env now
    #     #   any: reset all the env when any robot done
    #     #   all: reset all the env when all robots done
    #     #   single: reset one robot who has done, depending on the done list
    #     if mode == 'now':
    #         self.reset_all() 
    #     else:
    #         done_list = self.done_list(**kwargs)
    #         if mode == 'any' and any(done_list): self.reset_all()
    #         elif mode == 'all' and all(done_list): self.reset_all()
    #         elif mode == 'single': 
    #             [self.reset_single(i) for i, done in enumerate(done_list) if done]

    # def end(self, ani_name='animation', fig_name='fig.png', ending_time = 3, suffix='.gif', keep_len=30, rm_fig_path=True, fig_kwargs=dict(), ani_kwargs=dict(), **kwargs):
        
    #     # fig_kwargs: arguments when saving the figures for animation, see https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html for detail
    #     # ani_kwargs: arguments for animations(gif): see https://imageio.readthedocs.io/en/v2.8.0/format_gif-pil.html#gif-pil for detail
    #     if self.control_mode == 'keyboard': self.listener.stop()
        
    #     show = kwargs.get('show', self.display)
        
    #     if not self.disable_all_plot:

    #         if self.save_ani:
    #             saved_ani_kwargs = {'subrectangles': True}
    #             saved_ani_kwargs.update(ani_kwargs) 
    #             self.save_animate(ani_name, suffix, keep_len, rm_fig_path, **saved_ani_kwargs)

    #         if self.save_fig or show:
    #             self.draw_components(self.ax, mode='dynamic', **kwargs)
            
    #         if self.save_fig: 
    #             if not self.fig_path.exists(): self.fig_path.mkdir()

    #             self.fig.savefig(str(self.fig_path) + '/' + fig_name, bbox_inches=self.bbox_inches, dpi=self.fig_dpi, **fig_kwargs)

    #         if show:
    #             plt.show(block=False)
    #             print(f'Figure will be closed within {ending_time:d} seconds.')
    #             plt.pause(ending_time)
    #             plt.close()


    @property
    def robot(self):
        robot_list = [ obj for obj in self.objects if obj.role == 'robot']

        return robot_list[0]

    def get_current_robots(self):
        return [obj for obj in self.objects if obj.role == 'robot']

    def get_robot_state(self):
        return self.robot._sstate
    
    def get_lidar_scan(self, id=0):
        r_list = self.get_current_robots()

        return r_list[id].get_lidar_scan()


        

    


