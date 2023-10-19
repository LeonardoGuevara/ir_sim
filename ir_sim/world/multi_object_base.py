import numpy as np
from ir_sim.util.util import extend_list
from ir_sim.world.object_base import ObjectBase
from ir_sim.lib.generation import generate_polygon

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
            
        elif distribution_dict['mode'] == 'manual':
            # state_list = kwargs['states']
            state_list = kwargs.get('states', [[0, 0, 0]] * self.number)


        elif distribution_dict['mode'] == 'random':
            state_list = kwargs['states']


        shape_list = kwargs['shapes']


        # if distribution_dict.get('random_shape', False):
            
        #     temp_shape_list = kwargs['shapes']
        #     shape_list = []

        #     for shape_dict in temp_shape_list:
                
        #         if shape_dict['name'] == 'polygon':
                    
        #             shape_number = shape_dict.get('random_number', self.number)
        #             vertices_list = self.random_generate_polygon(shape_number, **distribution_dict)

        #             # poly_shape_list = extend_list([shape_dict], self.number)
        #             poly_shape_list = [ {'name': 'polygon', 'vertices': vertices_list[i]}  for i in range(shape_number) ]
        #             shape_list += poly_shape_list

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



    def random_generate_polygon(self, number=1, center_range=[0, 0, 10, 10], avg_radius_range=[0.1, 1], irregularity_range=[0, 1], spikiness_range=[0, 1], num_vertices_range=[4, 10], **kwargs):

        ''' 
        2d range: min_x, min_y, max_x, max_y
        '''
        
        center = np.random.uniform(low=center_range[0:2], high=center_range[2:], size=(number, 2))
        avg_radius = np.random.uniform(low=avg_radius_range[0], high=avg_radius_range[1], size=(number,))
        irregularity = np.random.uniform(low=irregularity_range[0], high=irregularity_range[1], size=(number,))
        spikiness = np.random.uniform(low=spikiness_range[0], high=spikiness_range[1], size=(number,))
        num_vertices = np.random.randint(low=num_vertices_range[0], high=num_vertices_range[1], size=(number,))

        vertices_list = [generate_polygon(center[i, :], avg_radius[i], irregularity[i], spikiness[i], num_vertices[i]) for i in range(number)]
        
        return vertices_list




        

            
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

       
    
        



        
        
        
    





    