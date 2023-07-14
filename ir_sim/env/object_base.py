
from typing import Any

import numpy as np
from shapely import Polygon, Point, MultiPolygon


class object_base:

    _id = 0

    def __init__(self, state, shape, static=False) -> None:

        '''
        properties of an object:
        -----------------------
            id: 
            geometry: constructed by shapely.      
            state: The state of the object, including: position and orientation, represented by a tuple (x, y, theta). 
            static: Whether static object. If static, the motion will not be considered, default is False.
            velocity:

        parameters:
        -----------
            coordinates: the coordinates of the object, a list of tuples.
            shape: the shape of the object, a string, including: circle, polygon.
      
        '''

        self._id = object_base._id
        self._geometry = None

        self.static = static


        object_base._id += 1
        

    def step(self, velocity):

        if self.static:
            return 

        else:  
            pass
    

    def construct_geometry(self, shape, coordinate):

        if shape == 'polygon':
            pass


        


    @property
    def geometry(self):
        return self._geometry

    @property
    def centroid(self):
        return self._geometry.centroid
        
    @property
    def id(self):
        return self._id
    
    def state(self):
        return self._state



    # Operators
