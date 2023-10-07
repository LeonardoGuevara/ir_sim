import numpy as np
from ir_sim.util.util import extend_list
from ir_sim.world.object_base import ObjectBase

class MultiObjects:
    def __init__(self, dynamics, number, distribution, **kwargs) -> None:
        
        self.number = number
        self.dynamics = dynamics

        # self.object_list = [object_class(**kwargs) for _ in range(number)]
        self.state_list, self.shape_list = self.generate_state_shape(distribution, **kwargs)

        behavior_list = kwargs.get('behaviors', [])
        self.behavior_list = extend_list(behavior_list, self.number)

        if self.behavior_list is None:

            self.object_list = [ ObjectBase.create_with_shape(dynamics, shape, state=state, **kwargs) for state, shape in zip(self.state_list, self.shape_list) ]

        else:
            self.object_list = [ ObjectBase.create_with_shape(dynamics, shape, state=state, behavior=behavior, **kwargs) for state, shape, behavior in zip(self.state_list, self.shape_list, self.behavior_list) ]




    def __add__(self, other):
        return self.object_list + other.object_list

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        return self.object_list[index]
    
    
    def generate_state_shape(self, distribution_dict, **kwargs):


        if distribution_dict is None:
            # default
            state_list = kwargs['states']
            shape_list = kwargs['shapes']

        elif distribution_dict['mode'] == 'manual':

            state_list = kwargs['states']
            shape_list = kwargs['shapes']

        elif distribution_dict['mode'] == 'random':
            pass
        

        if distribution_dict.get('random_shape', False):
            pass

        if distribution_dict.get('random_bear', False):
            pass

        
        state_list = extend_list(state_list, self.number)
        shape_list = extend_list(shape_list, self.number)
        
        return state_list, shape_list



    def step(self, velocity_list=[]):

        for obj, vel in  zip(self.object_list, velocity_list):
            obj.step(vel)


    def plot(self, ax, **kwargs):

        for obj in self.object_list:
            obj.plot(ax, **kwargs)


            
    # def set_attributes(self, **kwargs):
        
    #     states_kwargs = kwargs.get('states', dict())
    #     shapes_kwargs = kwargs.get('shapes', dict())

    #     self.set_states(**states_kwargs)
    #     self.set_shapes(**shapes_kwargs)

    # def set_states(self, mode='manual', random_bear=False, **kwargs):
        
    #     if mode == 'manual':
    #         default = [[i, 0] for i in range(self.number)]
    #         states = kwargs.get('states', default)
        
    #     elif mode == 'random':

    #         low = kwargs.get('low', [0, 0, 0])
    #         high = kwargs.get('high', [10, 10, 2*np.pi])

    #         states = np.random.uniform(low=low, high=high, size=(self.number, 2))

    #     elif mode == 'circular':
    #         pass
        

    #     states = extend_list(states, self.number)
    #     [obj.set_state(state) for obj, state in zip(self.object_list, states)]


    # def set_shapes(self, mode='manual', random_bear=False):
        
    #     if mode == 'manual':
    #         pass
        
    #     elif mode == 'random':
    #         pass 

       
    
        



        
        
        
    





    