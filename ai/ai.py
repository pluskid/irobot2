import re
import threading
from   threading import Thread

from   exception import IllegalOperation
from   event     import *
from   api       import State
import action

class StateRunner(Thread):
    class Stop(Exception):
        pass

    def __init__(self, robot, state):
        Thread.__init__(self)
        self._robot = robot
        self._state = state()
        self._stop = False
        self._event = threading.Event()

        self._state.run_action = self.run_action
        self._state.goto_state = self.goto_state

    def run_action(self, name, *args):
        if threading.currentThread() is not self:
            raise IllegalOperation('Action can only be run in loop')
        clsname = 'Ac' + name
        if not hasattr(action, clsname):
            raise IllegalOperation('No such action: %s' % name)
        cls = getattr(action, clsname)

        # pass action to robot
        self._robot['k.action'] = cls(self._robot, *args)
        # and then wait for action to finish
        self._event.wait()
        self._event.clear()
        # then we wake up, check if we should terminate
        if self._stop is True:
            raise StateRunner.Stop()

    def goto_state(self, state_name):
        pass

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
        if isinstance(event, EvBorn):
            self._robot['k.alive'] = True
            self._state_runner = StateRunner(self._robot, 
                                             self._states['Global'])
            self._state_runner.start_looping()
        elif isinstance(event, EvDeath):
            self._robot['k.alive'] = False
            self._state_runner.terminate_looping()
        elif isinstance(event, EvDone):
            self._state_runner.continue_looping()
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
