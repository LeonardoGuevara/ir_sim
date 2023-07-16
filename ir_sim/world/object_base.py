import numpy as np
from shapely import MultiPolygon, Point, Polygon, LineString
import itertools
from typing import Optional

class object_base:

    id_iter = itertools.count()

    def __init__(self, shape: str='circle', shape_tuple=None, state=[0, 0, 0], velocity=[0, 0], dynamics: str='omni', role: str='obstacle', static=False) -> None:

        '''
        parameters:
        -----------
            shape: the shape of the object, a string, including: circle, polygon, linestring,

            shape_tuple: tuple to init the geometry, default is None; A sequence of (x, y) numeric coordinate pairs or triples, or an array-like with shape (N, 2)
                for circle, the list should have be: (center, radius)
                for polygon, the list should have the element: [vertices], number of vertices >= 3
                for lineString, the list should have the element: [vertices]

            state: the state of the object, list or numpy. default is [0, 0, 0], [x, y, theta]

            velocity: the velocity of the object, list or numpy. default is [0, 0], [vx, vy]

            dynamics: the moving dynamics of the object, including omni, differential, ackermann, custom; default omni, if custom, 

            static: whether static object; default False

            role: the role of the object, including: robot, obstacle, landmark, target, default is 'obstacle'
        '''

        self._id = next(object_base.id_iter)
        self._shape = shape
        self._geometry = self.construct_geometry(shape, shape_tuple)

        self._state = state
        self._velocity = velocity

        self._dynamics = dynamics

        self.role = role
        self.static = static


    
    def step(self, velocity):

        if self.static:
            return  

        else:  
            pass
    

    def construct_geometry(self, shape, shape_tuple):

        if shape == 'circle':
            geometry = Point(shape_tuple[0]).buffer(shape_tuple[1])

        elif shape == 'polygon':
            geometry = Polygon(shape_tuple)

        elif shape == 'linestring':
            geometry = LineString(shape_tuple)

        else:
            raise ValueError("shape should be one of the following: circle, polygon, linestring")

        return geometry


    def state_transition(self):

        
        
        
        pass


        




    @property
    def shape(self):
        return self._shape

    @property
    def geometry(self):
        return self._geometry

    @property
    def centroid(self):
        return self._geometry.centroid
        
    @property
    def id(self):
        return self._id
    


    @property
    def state(self):
        return self._state




    # Operators

