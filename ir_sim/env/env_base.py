from ir_sim.util.util import file_check

class EnvBase:
    def __init__(self, world_name=None, ):

        self.world_name = file_check(world_name)
        


    


