from random import randint

from .api   import State
from ..util import vec2d

class StGlobal(State):
    def loop(self):
        friends, enemies = self.look_around()
        if len(enemies) != 0:
            self.run_action('ChangeState', 'Kill')
        self.run_action('PathTo', vec2d(randint(0, 500), randint(0, 500)))
        
    def on_collide(self, event):
        return 'Global'

class StKill(State):
    def loop(self):
        friends, enemies = self.look_around()
        if len(enemies) == 0:
            self.run_action('ChangeState', 'Global')
        else:
            enemy = enemies[0]
            self.run_action('ShootAt', enemy.position)

