from gym.envs.registration import registry, register, make, spec
register(
    id='scheduler-v0',
    entry_point='scheduler.envs:scheduler',
)

print ("inside scheduler\scheduler")

