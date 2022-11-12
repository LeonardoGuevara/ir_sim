from ir_sim2.env import EnvBase

env = EnvBase('render_world.yaml')

for i in range(3000):

    vel = env.cal_des_vel()
    env.step(vel)
    env.render(0.05, robot_color='g', show_traj=True, show_text=True, goal_color='r', show_goal=True, traj_type='-g', show_sensor=True, bbox_inches='tight', pad_inches=0)
    # env.render(0.05, show_trail=True, edgecolor='y', trail_type='rectangle')  for ackermann
    env.reset('single')  # 'all'; 'any'; 'single'

env.end(robot_color='g', show_traj=True, show_text=True, goal_color='r', show_goal=True, traj_type='-g')
