from   __future__ import with_statement
from   random     import randint

import yaml

from   irobot2.god    import God
from   irobot2.robot  import Robot
from   irobot2.util   import vec2d
from   irobot2.ai     import connect_states
from   irobot2.ai.ai  import parse_module
from   irobot2.ai.api import State

from   ai             import wasp, ruby

with open('game.yml') as ins:
    god = God(yaml.load(ins.read()))

#robot1 = god.build_robot('wasp', 'kid', 'Apache1')
robot2 = god.build_robot('ruby', 'kid', 'Apache2')
#robot3 = god.build_robot('wasp', 'kid', 'Apache3')

robot4 = god.build_robot('apache_II', 'kily', 'Ruby')

## state
states_wasp = parse_module(wasp)
states_ruby = parse_module(ruby)

#connect_states(robot1, states_wasp)
connect_states(robot2, states_ruby)
#connect_states(robot3, states_wasp)
connect_states(robot4, states_wasp)

god.start()

