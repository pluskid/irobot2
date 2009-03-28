from basic   import Action
from move    import AcTurn
from compose import SequenceAction

class AcShoot(Action):
    NOT_CHARGED = 0
    CHARGING    = 1
    CHARGED     = 2

    def __init__(self, robot, stype, strike):
        Action.__init__(self, robot)
        self._stype = stype
        self._strike = strike
        self._state = self.NOT_CHARGED

    def update(self, god, intv):
        if self._state == self.NOT_CHARGED:
            self._state = self.CHARGING
            config = god.config['setting']['shoots'][self._stype]
            self._charging_remain = config['charge']
            self.charge(intv)
        elif self._state == self.CHARGING:
            self.charge(intv)

        if self._state == self.CHARGED:
            position  = self._robot['k.position']
            direction = self._robot['k.direction']
            width = self._robot['k.sprite']._base_image.get_rect().width
            shoot_pos = position+direction.normalized()*(width/2)
            god.create_shoot(shoot_pos, direction,
                             self._robot['k.sprite'], 
                             self._stype, self._strike)
            return self.event_done()

    def charge(self, intv):
        self._charging_remain -= intv
        if self._charging_remain <= 0:
            self._state = self.CHARGED

class AcShootAt(Action):
    def __init__(self, robot, dest, stype, strike):
        Action.__init__(self, robot)
        aturn  = AcTurn(robot, dest-robot['k.position'])
        ashoot = AcShoot(robot, stype, strike)
        self._action = SequenceAction(robot, [aturn, ashoot])

    def update(self, god, intv):
        return self._action.update(god, intv)

