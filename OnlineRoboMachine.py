from random import choice
from robot.libraries.BuiltIn import BuiltIn

class OnlineRoboMachine(object):

    def __init__(self):
        self._actions = None

    def begin_actions(self):
        assert self._actions is None or self._actions.is_complete()
        self._actions = Actions()

    def act(self, *args):
        self._actions.add(args)

    def end_actions(self):
        self._actions.complete()

    def execute_mbt(self):
        while not self._actions.is_executed():
            self._actions.execute()


class Actions(object):

    def __init__(self):
        self._actions = []
        self._complete = False
        self._executed = False

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
        BuiltIn().run_keyword(*choice(self._actions))
        self._executed = True
