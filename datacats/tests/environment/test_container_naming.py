# Copyright 2014-2015 Boxkite Inc.

# This file is part of the DataCats package and is released under
# the terms of the GNU Affero General Public License version 3.0.
# See LICENSE.txt or http://www.fsf.org/licensing/licenses/agpl-3.0.html

from unittest import TestCase

from datacats.environment import Environment


class TestContainerNames(TestCase):
    def test_container_names(self):
        """
        Ensures container naming is handled correctly
        """
        # The only info it should use is the name
        empty_environment = Environment('testenv', None, None)
        self.assertEqual(Environment._get_container_name(empty_environment, 'solr'),
                         'datacats_solr_testenv')
