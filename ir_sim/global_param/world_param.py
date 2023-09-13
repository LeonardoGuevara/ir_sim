import os
import ir_sim

time = 0
control_mode = 'auto'
collision_mode = 'stop' #  None: No collision check
                    # stop (default): All Objects stop when collision, 
                    # react: robot will have reaction when collision with others

step_time = 0.1
count = 0

root_path = os.path.dirname(ir_sim.__file__)







