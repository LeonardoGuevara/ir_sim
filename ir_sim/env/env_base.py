import yaml

from ir_sim.util.util import file_check
from ir_sim.world import world

class EnvBase:

    '''
    The base class of environment.

        parameters:
            world_name: the name of the world file, default is None
    
    
    '''


    def __init__(self, world_name=None, **kwargs):

        world_file_path = file_check(world_name)
        
        if world_file_path != None:
           
            with open(world_file_path) as file:
                com_list = yaml.load(file, Loader=yaml.FullLoader)
                world_args = com_list.get('world', dict())

        world_args |= kwargs.get('world_args', dict())



        # init world, robot, obstacles
        self.world = world(**world_args)
    
    

    
    




    def show(self):
        pass



    def end(self):
        pass

    


