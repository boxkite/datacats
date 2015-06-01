from datacats.environment import Environment
from collections import defaultdict


class MockEnvironment(Environment):
    """
    A class that pretends to be an environment, while only allowing certain
    methods to run.
    """
    def __init__(self, *args, **kwargs):
        self.allow = ['__init__', '_choose_port']
        self.counts = defaultdict(int)
        super(MockEnvironment, self).__init__(*args, **kwargs)

    def trap_method(self, method):
        object.__getattribute__(self, 'counts')[method] += 1

    def __getattribute__(self, item):
        obj = object.__getattribute__(self, item)
        allows = object.__getattribute__(self, 'allow')
        if item not in allows and hasattr(obj, '__call__'):
            object.__getattribute__(self, 'trap_method')(item)

            def empty(*args, **kwargs):
                pass

            return empty
        else:
            return obj
