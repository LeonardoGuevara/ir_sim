import os
import sys
from math import pi, atan2, sin, cos
import numpy as np

def file_check(file_name):

    # check whether file exist or the type is correct'
    
    if file_name is None: return None
        
    if os.path.exists(file_name):
        abs_file_name = file_name
    elif os.path.exists(sys.path[0] + '/' + file_name):
        abs_file_name = sys.path[0] + '/' + file_name
    elif os.path.exists(os.getcwd() + '/' + file_name):
        abs_file_name = os.getcwd() + '/' + file_name
    else:
        abs_file_name = None
        raise FileNotFoundError("File not found: " + file_name)

    return abs_file_name


def WrapToPi(rad):
    # transform the rad to the range [-pi, pi]
    while rad > pi:
        rad = rad - 2 * pi
    
    while rad < -pi:
        rad = rad + 2 * pi
    
    return rad

def WrapToRegion(rad, range):
    # transform the rad to defined range, 
    # the length of range should be 2 * pi
    assert(len(range) >= 2 and range[1] - range[0] == 2*pi)

    while rad > range[1]:
        rad = rad - 2 * pi
    
    while rad < range[0]:
        rad = rad + 2 * pi
    
    return rad

def extend_list(input_list, number):

    if len(input_list) < number: 
        input_list.extend([input_list[-1]]* (number - len(input_list)) )

    return input_list

def relative_position(position1, position2, topi=True):

    diff = position2[0:2]-position1[0:2]
    distance = np.linalg.norm(diff)
    radian = atan2(diff[1, 0], diff[0, 0])

    if topi: radian = WrapToPi(radian)

    return distance, radian

def get_transform(state):
    # from state to rotation and transition matrix
    # state: (3, 1) or (2 ,1)
    if state.shape == (2, 1):
        rot = np.array([ [1, 0], [0, 1] ])
        trans = state[0:2]

    else:
        rot = np.array([ [cos(state[2, 0]), -sin(state[2, 0])], [sin(state[2, 0]), cos(state[2, 0])] ])
        trans = state[0:2]

    return trans, rot 

def get_affine_transform(state):
    # 2d: 6 paramters: [a, b, d, e, xoff, yoff] reference: https://shapely.readthedocs.io/en/stable/manual.html
    return [cos(state[2, 0]), -sin(state[2, 0]), sin(state[2, 0]), cos(state[2, 0]), state[0, 0], state[1, 0]]

