from god   import God
from robot import Robot
from util  import vec2d

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
god.add_robot(robot)
god.start()

