import re
import threading
from   threading   import Thread

from   pygame      import Rect

from   .ai_action  import perform_action
from   .api        import State
from   ..exception import IllegalOperation
from   ..event     import EvBorn, EvDeath, EvDone, EvChangeState
from   ..util      import DictObj, vec2d
from   ..robot     import Robot

class StateRunner(Thread):
    class Stop(Exception):
        pass

    def __init__(self, robot, state):
        Thread.__init__(self)
        self._robot = robot
        self._state = state()
        self._stop = False
        self._event = threading.Event()

        self._state.run_action  = self.run_action
        self._state.map_size    = self.map_size
        self._state.map_elem    = self.map_elem
        self._state.elem_size   = self.elem_size
        self._state.grid2point  = self.grid2point
        self._state.look_around = self.look_around
        self._state.get_info    = self.get_info

        self._state.get         = self.get
        self._state.put         = self.put

        # See http://blog.pluskid.org/?p=299
        def set_prop_getter(name):
            setattr(self._state, 'get_%s'%name,
                    lambda: self._robot['k.%s'%name])
        for prop in Robot.public_props:
            set_prop_getter(prop)

    def get(self, key):
        return self._robot['u.%s'%key]
    def put(self, key, val):
        self._robot['u.%s'%key] = val

    def run_action(self, name, *args, **kw):
        if threading.currentThread() is not self:
            raise IllegalOperation('Action can only be run in loop')
        # perform action
        perform_action(name, self._robot, *args, **kw)
        # and then wait for action to finish
        self._event.wait()
        self._event.clear()
        # then we wake up, check if we should terminate
        if self._stop is True:
            raise StateRunner.Stop()

    def look_around(self):
        sprites = self._robot['k.god'].robot_look_around(self._robot)
        robots = [self.collect_robot_info(r) for r in sprites]
        friends = []; enemies = []
        team = self._robot['k.team']
        for r in robots:
            if r.team == team:
                friends.append(r)
            else:
                enemies.append(r)
        return friends, enemies
    def get_info(self, team, name):
        robot = self._robot['k.god'].get_robot(team, name)
        if robot is not None and robot['k.alive']:
            eyesight = self._robot.eyesight_rect
            if team == self._robot['k.team'] or \
               eyesight.colliderect(robot['k.sprite'].bound_rect):
                return self.collect_robot_info(robot['k.sprite'])
        return None

    def collect_robot_info(self, sprite):
        # We collect thise information here instead of return 
        # the sprite directly or wrap it as a proxy to generate
        # those information lazily because we will not allow the
        # AI to access the sprite object direct. Or else, it can
        # do what ever it want to, e.g. sprite._robot['k.hp'] = 0
        robot = sprite._robot
        info = DictObj()
        for prop in Robot.public_props:
            info[prop] = robot['k.%s'%prop]
        return info

    def grid2point(self, grid, pos='center'):
        """\
        From grid coordinate to point coordinate.

         - grid: can either be a 2-tuple or vec2d or similar
         - pos: 'center' to return the center of the grid
                'top-left' to return the top-left point
        """
        grid_size = self.elem_size()
        x = grid[0]*grid_size[0]
        y = grid[1]*grid_size[1]
        if pos == 'center':
            x += grid_size[0]/2
            y += grid_size[1]/2
        return vec2d(x, y)

    def elem_size(self):
        map = self.game_map
        return map.tile_size
    def map_size(self):
        map = self.game_map
        return map.geometry
    def map_elem(self, x, y):
        map = self.game_map
        try:
            elem = map[x, y]
            if elem is None:
                return DictObj({'type': 'empty'})
            elif elem.type in ['box', 'treasure']:
                return DictObj({'type': elem.type, 'hp': elem.hp})
            elif elem.type == 'obstacle':
                return DictObj({'type': elem.type})
            
        except IndexError:
            return DictObj({'type': 'obstacle'})
        

    @property
    def game_map(self):
        god = self._robot['k.god']
        return god.game_map

    def run(self):
        loop_func = self._state.loop
        try:
            while True:
                loop_func()
        except StateRunner.Stop:
            pass

    def start_looping(self):
        self._state.initialize()
        self.start()
    def continue_looping(self):
        self._event.set()
    def terminate_looping(self):
        self._stop = True
        self._event.set()
        self.join()
        self._state.terminate()


class AI(object):
    def __init__(self, robot, states):
        self._robot = robot
        robot.assign_ai(self)
        self._states = states
        self._state_runner = None

    def process_event(self, event):
        new_state = None
        if isinstance(event, EvBorn):
            self._state_runner = StateRunner(self._robot, 
                                             self._states['Global'])
            self._state_runner.start_looping()
        elif isinstance(event, EvDeath):
            self._state_runner.terminate_looping()
        elif isinstance(event, EvDone):
            self._state_runner.continue_looping()
        elif isinstance(event, EvChangeState):
            new_state = event.state
        else:
            new_state = self._state_runner._state.handle_event(event)

        if new_state is not None:
            self._state_runner.terminate_looping()
            self._state_runner = StateRunner(self._robot,
                                             self._states[new_state])
            self._state_runner.start_looping()


def parse_module(module):
    states = {}
    pat_stname = re.compile(r'St(.*)')
    for attr in dir(module):
        mod = getattr(module, attr)
        res = pat_stname.match(attr)
        if res is not None and       \
           isinstance(mod, type) and \
           issubclass(mod, State):
            state_name = res.group(1)
            state = mod
            states[state_name] = mod
    return states
