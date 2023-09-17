import numpy as np
from ir_sim.world.obstacles.obstacle_diff import ObstacleDiff
from ir_sim.world.obstacles.obstacle_static import ObstacleStatic


class ObstacleFactory:

    def create_obstacle(self, dynamics=None, shape=dict(), **kwargs):

        if dynamics == 'diff':
            return ObstacleDiff.create_with_shape(dynamics, shape, **kwargs)
        elif dynamics == 'acker':
            pass
        elif dynamics == 'omni':
            pass
        else:
            return ObstacleStatic.create_with_shape(dynamics, shape, **kwargs)
            
            
        
    # def __init__(self, type='diff', shape='circle', **kwargs) -> None:
        

    
        
