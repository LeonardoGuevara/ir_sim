import sys
from dataclasses import dataclass

@dataclass
class PathManager:
    root_path: str = sys.path[0]
    ani_buffer_path: str = sys.path[0] + '/animation_buffer'
    ani_path: str = sys.path[0] + '/animation'
    fig_path: str = sys.path[0] + '/figure'


path_manager = PathManager()

