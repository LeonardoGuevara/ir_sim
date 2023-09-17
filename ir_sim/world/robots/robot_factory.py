import numpy as np
from ir_sim.world.robots.robot_diff import RobotDiff
from ir_sim.world.robots.robot_acker import RobotAcker
from ir_sim.world import ObjectBase


class RobotFactory:

    def create_robot(self, dynamics='diff', shape=dict(), **kwargs) -> ObjectBase:

        if dynamics == 'diff':
            return RobotDiff.create_with_shape('diff', shape, **kwargs)
        elif dynamics == 'acker':
            return RobotAcker.create_with_shape('acker', shape, **kwargs)
        elif dynamics == 'omni':
            # return RobotOmni(**kwargs)
            pass
        else:
            raise NotImplementedError(f"Robot dynamics {dynamics} not implemented")
    
    
    
            
        
    # def __init__(self, type='diff', shape='circle', **kwargs) -> None:
        

    
        
