from basic import Action

class AcShoot(Action):
    def __init__(self, robot, stype):
        Action.__init__(self, robot)
        self._stype = stype

    def update(self, god, intv):
        position  = self._robot['k.position']
        direction = self._robot['k.direction']
        width = self._robot['k.sprite']._base_image.get_rect().width
        shoot_pos = position+direction.normalized()*(width/2)
        god.create_shoot(shoot_pos, direction, self._robot['k.sprite'], self._stype)
        return self.event_done()
        
