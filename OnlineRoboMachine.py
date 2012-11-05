#  Copyright 2012 Mikko Korpela
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from itertools import takewhile
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

    def act(self, *args):
        """
        Create a new action in the action block.

        args must contain ==> symbol
        act  TRANSITION  ==>  END STATE
        TRANSITION is a keyword call - can be omitted
        END STATE is a keyword call
        """
        assert len(args) - 1 > len(list(takewhile(lambda x: x != '==>', args)))
        self._actions.add(args)

    def act_if(self, condition, keyword, *args):
        """
        Create a new action in the action block if the condition holds.

        """
        if BuiltIn()._is_true(condition):
            self.act(keyword, *args)

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
        action = self._random.any_of(*self._actions)
        first = list(takewhile(lambda x: x != '==>', action))
        if first:
            BuiltIn().run_keyword(*first)
        BuiltIn().run_keyword(*action[len(first)+1:])
