from ir_sim.world import ObjectBase


class RobotDiff(ObjectBase):
    def __init__(self, shape='circle', shape_tuple=None, **kwargs):
        super(RobotDiff, self).__init__(shape=shape, shape_tuple=shape_tuple, dynamics='diff', role='robot', **kwargs)


    @classmethod
    def create_with_shape(cls, shape_dict, **kwargs):

        shape_name = shape_dict.get('name', 'circle')   
             
        if shape_name == 'circle':

            radius = shape_dict.get('radius', 0.2) 

            return cls(shape='circle', shape_tuple=(0, 0, radius), **kwargs)

        elif shape_name == 'rectangle':

            length = shape_dict.get('length', 0.2)
            width = shape_dict.get('width', 0.1)

            return cls(shape='polygon', shape_tuple=[(-length/2, -width/2), (length/2, -width/2), (length/2, width/2), (-length/2, width/2)], **kwargs)

        else:
            raise NotImplementedError(f"Robot shape {shape_name} not implemented")

  
# shape='circle', shape_tuple=(0, 0, radius), dynamics='diff', role='robot', **kwargs

    def plot(self, ax, show_goal=True, show_arrow=True, **kwargs):
        super().plot(ax, show_goal=show_goal, show_arrow = show_arrow, **kwargs)


    






        








