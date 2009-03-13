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

robot1 = god.build_robot('wasp', 'kid', 'Apache')
robot1['k.position'] = vec2d(500, 400)

robot2 = god.build_robot('apache_II', 'kid', 'Ruby')
robot2['k.position'] = vec2d(300, 300)

## state
states = parse_module(example)

connect_states(robot1, states)
connect_states(robot2, states)

god.start()

