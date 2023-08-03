import yaml

from ir_sim.util.util import file_check
from ir_sim.world import world, MultiRobots
from env_plot import EnvPlot


class EnvBase:

    '''
    The base class of environment.

        parameters:
            world_name: the name of the world file, default is None
    
    
    '''


    def __init__(self, world_name=None, **kwargs):

        world_file_path = file_check(world_name)
        
        world_kwargs, plot_kwargs = dict(), dict()


        if world_file_path != None:
           
            with open(world_file_path) as file:
                com_list = yaml.load(file, Loader=yaml.FullLoader)
                world_kwargs = com_list.get('world', dict())

        world_kwargs |= kwargs.get('world', dict())
        plot_kwargs |= kwargs.get('plot', dict())
        

        # init world, robot, obstacles
        self.world = world(**world_kwargs)
        self.robots = MultiRobots()
        # self.obstacles = MultiObstacles()
        # self.objects = self.robots.objects + self.obstacles.objects
        
        self.env_plot = EnvPlot(grid_map=self.world.grid_map, objects=self.objects, **plot_kwargs)




    def show(self):
        pass



    def end(self):
        pass

    


