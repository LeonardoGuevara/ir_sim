import numpy as np
from ir_sim.util.util import extend_list

class MultiObjects:
    def __init__(self, object_class, number, **kwargs) -> None:
        
        self.number = number
        self.object_list = [object_class(**kwargs) for i in range(number)]

        self.set_attributes(**kwargs)


    def __add__(self, other):
        return self.object_list + other.object_list

    def __len__(self):
        return len(self.object_list)

    def set_attributes(self, **kwargs):
        
        states_kwargs = kwargs.get('states', dict())
        shapes_kwargs = kwargs.get('shapes', dict())

        self.set_states(**states_kwargs)
        self.set_shapes(**shapes_kwargs)


    
    def set_states(self, mode='manual', random_bear=False, **kwargs):
        
        if mode == 'manual':
            default = [[i, 0] for i in range(self.number)]
            states = kwargs.get('states', default)
        
        elif mode == 'random':

            low = kwargs.get('low', [0, 0, 0])
            high = kwargs.get('high', [10, 10, 2*np.pi])

            states = np.random.uniform(low=low, high=high, size=(self.number, 2))

        elif mode == 'circular':
            pass
        

        states = extend_list(states, self.number)
        [obj.set_state(state) for obj, state in zip(self.object_list, states)]


    def set_shapes(self, mode='manual', random_bear=False):
        
        if mode == 'manual':
            pass
        
        elif mode == 'random':
            pass 

       
    
        



        
        
        
    





    