from ir_sim.lib.dynamics import differential_wheel_dynamics, ackermann_dynamics

dynamics_factory = {'diff': differential_wheel_dynamics, 'acker': ackermann_dynamics}