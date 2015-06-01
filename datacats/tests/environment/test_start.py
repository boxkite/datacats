import unittest

from datacats.tests.environment.mock_environment import MockEnvironment


class TestStart(unittest.TestCase):
    def setUp(self):
        self.environment = MockEnvironment.new('test', '2.3')

    def test_start(self):
        # Permit this method to run
        self.environment.allow.append('start_web')
        self.environment.start_web(production=True)
        self.environment.allow.pop()
        self.failUnless(self.environment.counts['_run_web_container'])
