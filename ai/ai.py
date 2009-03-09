import threading
from   threading import Thread

from   exception import IllegalOperation
from   event     import *
import action

class StateRunner(Thread):
    class Stop(Exception):
        pass

    def __init__(self, robot, state):
        Thread.__init__(self)
        self._robot = robot
        self._state = state
        self._stop = False
        self._event = threading.Event()

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

    def run(self):
        loop_func = self._state['loop']
        try:
            while True:
                loop_func(self.run_action)
        except StateRunner.Stop:
            pass

    def start_looping(self):
        initializer = self._state['initialize']
        initializer()
        self.start()
    def continue_looping(self):
        self._event.set()
    def terminate_looping(self):
        self._stop = True
        self._event.set()
        self.join()
        finalizer = self._state['terminate']
        finalizer()


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
        # TODO: else: event handler of state


