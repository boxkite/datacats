# Copyright 2014-2015 Boxkite Inc.

# This file is part of the DataCats package and is released under
# the terms of the GNU Affero General Public License version 3.0.
# See LICENSE.txt or http://www.fsf.org/licensing/licenses/agpl-3.0.html

"""
The commands module defines the datacats package's interface, that is
all the commands the package implements as functions.

The rest of the datacats package is
 - implementation of these commands
 - a shell wrapper of these commands for datacats-cli tool (see cli module)
"""
from datacats.environment import Environment
from datacats.util import function_as_step, run_a_sequence_of_function_steps
import task


def create(environment_dir, port, ckan_version, create_skin,
    site_name, start_web, create_sysadmin, address, log_syslog=False,
    datapusher=True, site_url=None, progress_tracker=None):
    environment = Environment.new(
        environment_dir,
        ckan_version,
        site_name,
        address=address,
        port=port)
    try:
        # There are a lot of steps we can/must skip if we're making a sub-site only
        making_full_environment = not environment.data_exists()

        steps = [
            function_as_step(
                lambda: environment.create_directories(making_full_environment),
                description="Create the directories"),
            environment.create_bash_profile
            ]
        if making_full_environment:
            steps += [
                environment.create_virtualenv,
                environment.save,
                function_as_step(lambda: environment.create_source(datapusher),
                    description="Create source"),
                environment.create_ckan_ini]

        steps += [
            environment.save_site,
            environment.start_supporting_containers,
            environment.fix_storage_permissions,
            function_as_step(
                lambda: environment.update_ckan_ini(skin=create_skin),
                description="Create ckan INI file")]

        if create_skin and making_full_environment:
            steps.append(environment.create_install_template_skin)

        steps.append(function_as_step(
            lambda: task.finish_init(
                environment, start_web, create_sysadmin, address,
                log_syslog=log_syslog, site_url=site_url),
            description="Starting the site"))

        run_a_sequence_of_function_steps(steps, progress_tracker=progress_tracker)
        if hasattr(progress_tracker, "clean_up"):
            progress_tracker.clean_up()

    except:
        if hasattr(progress_tracker, "clean_up"):
            progress_tracker.clean_up()
        raise
