from random         import randint

from irobot2.ai.api import State
from irobot2.util   import vec2d

class StGlobal(State):
    def loop(self):
        friends, enemies = self.look_around()
        if len(enemies) != 0:
            enemy = enemies[0]
            self.put('the-enemy.team', enemy.team)
            self.put('the-enemy.name', enemy.name)
            self.run_action('ChangeState', 'Kill')
        new_pos = self.position+vec2d(randint(0, 100), randint(0, 100))
        self.run_action('PathTo', new_pos)

    def on_collide(self, event):
        return 'Global'

class StKill(StGlobal):
    def loop(self):
        team = self.get('the-enemy.team')
        name = self.get('the-enemy.name')
        enemy = self.get_info(team, name)
        if enemy is None:
            self.run_action('ChangeState', 'Global')
        else:
            self.run_action('ShootAt', enemy.position)

