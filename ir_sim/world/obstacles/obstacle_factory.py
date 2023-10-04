import numpy as np
from ir_sim.world.obstacles.obstacle_diff import ObstacleDiff
from ir_sim.world.obstacles.obstacle_static import ObstacleStatic


class ObstacleFactory:

    def create_obstacle(self, dynamics_dict, shape=dict(), **kwargs):
        
        dynamics_name = dynamics_dict.pop('name', 'diff')
        # dynamics_name, dynamics_dict=dict(),  

        if dynamics_name == 'diff':
            return ObstacleDiff.create_with_shape(dynamics_name, shape, dynamics_dict=dynamics_dict, **kwargs)
        elif dynamics_name == 'acker':
            pass
        elif dynamics_name == 'omni':
            pass
        else:
            return ObstacleStatic.create_with_shape(dynamics_name, shape, dynamics_dict=dynamics_dict, **kwargs)
             

    def create_obstacle_single(self, dynamics=None, shape=dict(), **kwargs):

        if dynamics is None:
            return ObstacleStatic.create_with_shape(None, shape, dynamics_dict=dict(), **kwargs)

        dynamics_name = dynamics.pop('name', 'omni')
        
        if dynamics_name == 'diff':
            return ObstacleDiff.create_with_shape('diff', shape, dynamics_dict=dynamics, **kwargs)
        elif dynamics_name == 'acker':
            pass
        elif dynamics_name == 'omni':
            # return RobotOmni(**kwargs)
            pass
        



    # def __init__(self, type='diff', shape='circle', **kwargs) -> None:
        

    
        
