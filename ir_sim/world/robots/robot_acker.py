from ir_sim.world import ObjectBase


class RobotAcker(ObjectBase):
    def __init__(self, shape='rectangle', shape_tuple=None, **kwargs):
        super(RobotAcker, self).__init__(shape=shape, shape_tuple=shape_tuple, dynamics='diff', role='robot', **kwargs)


    @classmethod
    def construct_with_shape(cls, shape, **kwargs):

        if shape == 'circle':

            radius = kwargs.get('radius', 0.2) 

            return cls(shape='circle', shape_tuple=(0, 0, radius), **kwargs)

        elif shape == 'rectangle':

            length = kwargs.get('length', 0.2)
            width = kwargs.get('width', 0.1)

            return cls(shape='polygon', shape_tuple=[(-length/2, -width/2), (length/2, -width/2), (length/2, width/2), (-length/2, width/2)], **kwargs)


        
# shape='circle', shape_tuple=(0, 0, radius), dynamics='diff', role='robot', **kwargs

    def plot(self):
        pass







        








