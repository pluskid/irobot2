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
        return ('change', 'Global')

class StKill(StGlobal):
    def loop(self):
        team = self.get('the-enemy.team')
        name = self.get('the-enemy.name')
        enemy = self.get_info(team, name)
        if enemy is None:
            self.run_action('ChangeState', 'Global')
        else:
            direction = enemy.position - self.position
            pos = enemy.position - direction.normalized()*150
            pos += (randint(-80, 80), randint(-20, 20))
            if (pos-self.position).length > 40:
                self.run_action('MoveTo', pos)
                enemy = self.get_info(self.get('the-enemy.team'),
                                      self.get('the-enemy.name'))
            if enemy is not None:
                for rep in range(3):
                    print 'Shoot %d' % rep
                    self.run_action('ShootAt', enemy.position, type='laser')
            else:
                self.run_action('ChangeState', 'Global')

    def on_collide(self, event):
        return ('continue',)
