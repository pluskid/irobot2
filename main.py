from   __future__ import with_statement
from   random     import randint

import yaml

from   god        import God
from   robot      import Robot
from   util       import vec2d
from   ai         import connect_states
from   ai         import example
from   ai.ai      import parse_module
from   ai.api     import State

with open('game.yml') as ins:
    god = God(yaml.load(ins.read()))

rpropos = {
        'k.position': vec2d(500, 400),
        'k.direction': vec2d(1, 0),
        'k.alpha': 255,
        'k.team': 'kid',
        'k.name': 'Apache',
        'k.speed': 0.1,
        'k.angle_speed': 0.3,
        'k.hp': 500
        }
robot = Robot(rpropos)


## state
states = parse_module(example)

connect_states(robot, states)

god.add_robot(robot)
god.start()

