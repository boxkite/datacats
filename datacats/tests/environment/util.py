"""
This module contains some drop-dead simple implementations of
datacats features so that we can "mock" them.
"""

from docker.client import Client
from docker.utils import kwargs_from_env
from docker.errors import APIError

from shutil import rmtree
from os.path import expanduser, join as path_join, exists as path_exists

from datacats.docker import MINIMUM_API_VERSION


def _make_container_name(name, service):
    """
    Get a container name from a name
    :param service: The name of the service to get.
    :param name: The name of the environment.
    :return:
    """
    return "datacats_{}_{}".format(service, name)


def _make_docker_client():
    """
    Makes a Docker-py client object with the environment settings.
    :return: A docker-py Client object.
    """
    return Client(version=MINIMUM_API_VERSION, **kwargs_from_env())


def has_container(name, client=None):
    """
    Returns True if a container exists in any state, and False otherwise.
    :param name: The name of the container.
    :param client: Optional parameter specifying a client to use.
                   One will be created if not specified.
    :return: True of the container specified by 'name' exists, False otherwise.
    """
    # Reuse client if possible
    if not client:
        client = _make_docker_client()

    try:
        return client.inspect_container(name) is not None
    except APIError:
        return False


def is_boot2docker():
    """
    Returns True iff the current Docker server is running on a boot2docker VM.
    :return: True of the current Docker server specified in the environment is a
             boot2docker VM.
    """
    return 'Boot2Docker' in _make_docker_client().info()['OperatingSystem']


def purge(env_name):
    """
    This is a simple purge which expects that the environment named by 'env_name'
    has a source directory that is in the current directory.
    :param env_name: The name of the environment.
    :return: None.
    """
    client = _make_docker_client()

    # The first step - take out the containers. To avoid the problem of boot2docker,
    # we just check if they exist and don't try to nuke them if they don't.
    containers = ['postgres', 'pgdata', 'solr', 'web', 'venv']
    for container in containers:
        full_name = _make_container_name(env_name, container)

        if has_container(full_name, client=client):
            client.stop(full_name)
            client.remove_container(full_name)

    # TODO: This will fail on Linux because of the bad group on the postgres folder...
    datadir = expanduser(path_join('~', '.datacats', env_name))
    source_dir = expanduser(env_name)
    if path_exists(datadir):
        rmtree(expanduser(datadir))
    if path_exists(source_dir):
        rmtree(expanduser(source_dir))
