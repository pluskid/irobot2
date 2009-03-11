from random import randint

from ai.api import State

class StGlobal(State):
    def loop(self):
        self.run_action('MoveTo', vec2d(randint(0, 500), randint(0, 500)))
        
    def on_collide(self, event):
        self.goto_state('Global')
