from random import randint

from .api   import State
from ..util import vec2d

class StGlobal(State):
    def loop(self):
        self.run_action('MoveTo', vec2d(randint(0, 500), randint(0, 500)))
        robots = self.look_around()
        if len(robots) != 0:
            enemy = robots[0]
            print '%s: %s at %s' % (self.get_name(), 
                                    enemy.name, enemy.position)
            for i in range(10):
                self.run_action('ShootAt', enemy.position)
        
    def on_collide(self, event):
        return 'Global'
