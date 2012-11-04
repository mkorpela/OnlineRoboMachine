from random import Random
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import time

class OnlineRoboMachine(object):

    def __init__(self, seed=None):
        self._seed = self._get_seed(seed)
        self._random = None
        self._actions = None

    def _get_seed(self, seed):
        if seed is not None:
            return float(seed)
        return time.time()

    def begin_actions(self):
        """
        Marks the start of a new actions block.
        """
        assert self._actions is None or self._actions.is_complete()
        self._actions = Actions(self)

    def act(self, keyword, *args):
        """
        Create a new action in the action block.

        """
        self._actions.add([keyword]+list(args))

    def end_actions(self):
        """
        Marks the end of the action block.
        """
        self._actions.complete()

    def execute_MBT(self):
        """
        Executes MBT test.

        Should be only called once.
        """
        logger.info('Executing random walk with seed %f' % self._seed)
        self._random = Random(self._seed)
        while not self._actions.is_executed():
            self._actions.execute()

    def any_of(self, *choices):
        """
        Select randomly one of the choices given as an arguments

        Can be called only after Execute MBT has been called.
        """
        assert self._random is not None
        return self._random.choice(choices)


class Actions(object):

    def __init__(self, random):
        self._actions = []
        self._complete = False
        self._executed = False
        self._random = random

    def add(self, args):
        assert not self._complete
        self._actions += [args]

    def complete(self):
        self._complete = True

    def is_complete(self):
        return self._complete

    def is_executed(self):
        return self._executed

    def execute(self):
        self._executed = True
        BuiltIn().run_keyword(*self._random.any_of(*self._actions))
