from random import randint

from god    import God
from robot  import Robot
from util   import vec2d
from ai     import connect_states
from ai.api import State

god = God('default.ini')

rpropos = {
        'k.position': vec2d(500, 400),
        'k.direction': vec2d(1, 0),
        'k.alpha': 255,
        'k.team': 'kid',
        'k.name': 'Apache',
        'k.speed': 0.1,
        'k.angle_speed': 0.3
        }
robot = Robot(rpropos)


## state
class StGlobal(State):
    def loop(self, run_action):
        if randint(0, 1) == 0:
            run_action('Shift', vec2d(randint(0, 500), randint(0, 500)))
        else:
            run_action('MoveTo', vec2d(randint(0, 500), randint(0, 500)))

states = {'Global': StGlobal()}

connect_states(robot, states)

god.add_robot(robot)
god.start()

