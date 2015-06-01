# Copyright 2014-2015 Boxkite Inc.

# This file is part of the DataCats package and is released under
# the terms of the GNU Affero General Public License version 3.0.
# See LICENSE.txt or http://www.fsf.org/licensing/licenses/agpl-3.0.html

from unittest import TestCase

import sys
import os
from os.path import exists as path_exists, expanduser, join as path_join

from datacats.tests.environment.util import purge, is_boot2docker

from datacats.cli.create import create_environment
from datacats.error import DatacatsError

ENV_NAME = 'createunittestenv'


class TestCreate(TestCase):
    def setUp(self):
        purge(ENV_NAME)

    def test_create(self):
        """
        Tests the creation of containers.
        """
        old_stdout = sys.stdout
        try:
            # Swallow all the (non-optional) output.
            sys.stdout = open(os.devnull, 'w')
            create_environment(ENV_NAME, None, '2.3', False, False, False, None)
        except DatacatsError as e:
            sys.stdout = old_stdout
            self.fail(str(e))
        finally:
            # Fix the stdout
            sys.stdout = old_stdout

        self.assert_(path_exists(expanduser(ENV_NAME)))
        self.assert_(path_exists(expanduser(path_join('~', '.datacats', ENV_NAME))))
        if not is_boot2docker():
            self.assert_(path_exists(expanduser(path_join('~', '.datacats', ENV_NAME, 'postgres'))))
        self.assert_(path_exists(expanduser(path_join('~', '.datacats', ENV_NAME, 'solr'))))

    def tearDown(self):
        purge(ENV_NAME)
