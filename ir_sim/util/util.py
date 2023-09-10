import os
import sys
from math import pi, atan2
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
