from random         import randint, choice

from irobot2.ai.api import State
from irobot2.util   import vec2d

class StGlobal(State):
    def initialize(self):
        size = self.map_size()
        self.pos_candidates = [(0, 0),
                               (size[0]-1, 0),
                               (size[0]-1, size[1]-1),
                               (0, size[1]-1),
                               (size[0]/2, size[1]/2)]

    def loop(self):
        friends, enemies = self.look_around()
        if len(enemies) != 0:
            enemy = enemies[0]
            self.run_action('ChangeState', 'MoveAround', 
                            self.calc_good_pos(enemy),
                            enemy.team, enemy.name)
        new_pos = self.grid2point(choice(self.pos_candidates))
        self.run_action('PathTo', new_pos)

    def on_collide(self, event):
        return ('change', 'Global')


    def calc_good_pos(self, enemy):
        dir = (self.position-enemy.position).normalized()
        return enemy.position + dir.rotated(randint(-40, 40))*100

class StMoveAround(StGlobal):
    def __init__(self, pos, team, name):
        self._pos = pos
        self._ntry = 0
        self._team = team
        self._name = name

    def loop(self):
        self._ntry += 1
        if self._ntry == 1:
            self.run_action('MoveTo', self._pos)
        elif self._ntry < 5:
            self.run_action('PathTo', self._pos)
        else:
            self.run_action('ChangeState', 'ShootAt', 
                            self._team, self._name)

    def on_collide(self, event):
        return ('continue',)

class StShootAt(StGlobal):
    def __init__(self, team, name):
        self._team = team
        self._name = name

    def loop(self):
        target = self.get_info(self._team, self._name)
        if target is None:
            self.run_action('ChangeState', 'Global')
        else:
            self.run_action('ShootAt', target.position, 'laser')

    def on_hurt(self, event):
        target = self.get_info(self._team, self._name)
        if target is None:
            return ('change', 'Global')
        else:
            return ('change', 'MoveAround',
                    self.calc_good_pos(target),
                    self._team, self._name)

