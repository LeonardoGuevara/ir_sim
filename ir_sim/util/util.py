import os
import sys

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
