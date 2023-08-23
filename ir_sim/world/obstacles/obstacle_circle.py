from math import inf, pi
from ir_sim.world import ObjectBase


class ObsCirle(ObjectBase):

    def __init__(self, shape: str = 'circle', shape_tuple=(0, 0, 0.2), state=..., velocity=..., dynamics: str = 'omni', role: str = 'obstacle', color='k', static=True) -> None:
        super().__init__(shape, shape_tuple, state, velocity, dynamics, role, color, static)

        





    def plot(self, ax):
        pass

    