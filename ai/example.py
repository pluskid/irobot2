from random import randint

from api  import State
from util import vec2d

class StGlobal(State):
    def loop(self):
        if randint(0, 100) < 40:
            self.run_action('Shoot')
        else:
            self.run_action('MoveTo', vec2d(randint(0, 500), randint(0, 500)))
        
    def on_collide(self, event):
        return 'Global'
