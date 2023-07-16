import itertools
from ir_sim.util.util import file_check



class world:
    def __init__(self, height=10, width=10, step_time=0.1, sample_time=0.1, offset=[0, 0]) -> None:
        
        '''
        the world object is the main object of the simulation, it manages all the other objects and maps in the simulation

        Parameters:
            height: the height of the world
            width: the width of the world
            step_time: the time interval between two steps
            sample_time: the time interval between two samples
        '''

        self.height = height
        self.width = width
        self.step_time = step_time
        self.sample_time = sample_time
        self.offset = offset

        self.count = 0
        self.sampling = True


    def step(self):

        self.count += 1
        self.sampling = (self.count % (self.sample_time / self.step_time) == 0)


    

    


    

