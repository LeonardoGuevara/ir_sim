from ir_sim.world import ObjectBase

class RobotDiffCirle(ObjectBase):
    def __init__(self, radius, **kwargs):
        super(RobotDiffCirle, self).__init__(shape='circle', shape_tuple= dynamics='differential', role='robot', **kwargs)

        








