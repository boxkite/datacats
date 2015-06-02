from unittest import TestCase
from docker.utils import kwargs_from_env
from docker.client import Client


class TestOpenSSLBug(TestCase):
    """
      Tests if communication between Docker and datacats fails
      (There could be various reasons for that like:
         1) Docker not installed properly
         2) Docker's envvariable not set up
         3) that weird bug one gets on MacOSX
         (see https://github.com/datacats/datacats/issues/63)

      None of these are really datacats issue per ce,
      still, should be useful
    """

    def test_docker_connection(self):
        try:
            kwargs = kwargs_from_env()
            client = Client(**kwargs)
            client.version()
        except Exception as e:
            self.fail("Cannot connect to Docker: " + e.__str__())
