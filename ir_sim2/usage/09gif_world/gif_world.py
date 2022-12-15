from ir_sim2.env import EnvBase
from pathlib import Path

env = EnvBase('gif_world.yaml', plot=True, display=False, save_ani=True, full=False)
# env = EnvBase('gif_world.yaml', save_ani=True, full=False, image_path='./test', ani_path=Path('./test2'))

for i in range(100):

    vel = env.cal_des_vel()
    env.step(vel)

    env.render(show_text=True, bbox_inches='tight', dpi=300)
    env.reset('single') 

env.end(ani_name='gif_world', show_text=True)
# env.end(ani_name='gif_world_duration', show_text=True, show=False, ani_args={'duration': 1})
# ani_args for GIF animation: https://imageio.readthedocs.io/en/v2.8.0/format_gif-pil.html#gif-pil

