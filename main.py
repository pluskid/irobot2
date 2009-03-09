from random import randint

from god   import God
from robot import Robot
from util  import vec2d
from ai    import connect_states

god = God('default.ini')

rpropos = {
        'k.position': vec2d(500, 400),
        'k.direction': vec2d(1, 0),
        'k.team': 'kid',
        'k.name': 'Apache',
        'k.speed': 0.1,
        'k.angle_speed': 0.3
        }
robot = Robot(rpropos)

## state
def st_init():
    pass
def st_term():
    pass
def st_loop(run_action):
    run_action('MoveTo', vec2d(randint(0, 500), randint(0, 500)))
states = {
        'Global': {
            'initialize': st_init,
            'loop': st_loop,
            'terminate': st_term
            }
        }
connect_states(robot, states)

god.add_robot(robot)
god.start()

