# Copyright 2014-2015 Boxkite Inc.

# This file is part of the DataCats package and is released under
# the terms of the GNU Affero General Public License version 3.0.
# See LICENSE.txt or http://www.fsf.org/licensing/licenses/agpl-3.0.html

import sys
import types
from os.path import abspath

import datacats
from datacats.error import DatacatsError

from datacats.cli.util import CLIProgressTracker, y_or_n_prompt, confirm_password
from datacats.task import finish_init


def write(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def create(opts):
    """Create a new environment

Usage:
  datacats create [-bin] [-s NAME] [--address=IP] [--syslog] [--ckan=CKAN_VERSION]
                  [--no-datapusher] [--site-url SITE_URL] ENVIRONMENT_DIR [PORT]

Options:
  --address=IP            Address to listen on (Linux-only) [default: 127.0.0.1]
  --ckan=CKAN_VERSION     Use CKAN version CKAN_VERSION [default: 2.3]
  -b --bare               Bare CKAN site with no example extension
  -i --image-only         Create the environment but don't start containers
  -n --no-sysadmin        Don't prompt for an initial sysadmin user account
  -s --site=NAME          Pick a site to create [default: primary]
  --no-datapusher         Don't install/enable ckanext-datapusher
  --site-url SITE_URL     The site_url to use in API responses (e.g. http://example.org:{port}/)
  --syslog                Log to the syslog

ENVIRONMENT_DIR is a path for the new environment directory. The last
part of this path will be used as the environment name.
"""

    progress_tracker = CLIProgressTracker(
        task_title='Creating datacats site environment')

    return datacats.create(
        environment_dir=opts['ENVIRONMENT_DIR'],
        port=opts['PORT'],
        create_skin=not opts['--bare'],
        start_web=not opts['--image-only'],
        create_sysadmin=not opts['--no-sysadmin'],
        site_name=opts['--site'],
        ckan_version=opts['--ckan'],
        address=opts['--address'],
        log_syslog=opts['--syslog'],
        datapusher=not opts['--no-datapusher'],
        site_url=opts['--site-url'],
        progress_tracker=progress_tracker
        )




def reset(environment, opts):
    """Resets a site to the default state. This will re-initialize the
database and recreate the administrator account.

Usage:
  datacats reset [-yn] [-s NAME] [ENVIRONMENT]

Options:
  -s --site=NAME          The site to reset [default: primary]
  -y --yes                Respond yes to all questions
  -n --no-sysadmin        Don't prompt for a sysadmin password"""
    # pylint: disable=unused-argument
    if not opts['--yes']:
        y_or_n_prompt('Reset will remove all data related to the '
                      'site {} and recreate the database'.format(opts['--site']))

    print 'Resetting...'
    environment.stop_supporting_containers()
    environment.stop_ckan()
    environment.purge_data([opts['--site']], never_delete=True)
    init({
        'ENVIRONMENT_DIR': opts['ENVIRONMENT'],
        '--site': opts['--site'],
        'PORT': None,
        '--syslog': None,
        '--address': '127.0.0.1',
        '--image-only': False,
        '--no-sysadmin': opts['--no-sysadmin'],
        '--site-url': None
        }, no_install=True)


def init(opts, no_install=False, quiet=False):
    """Initialize a purged environment or copied environment directory

Usage:
  datacats init [-in] [--syslog] [-s NAME] [--address=IP]
                [--site-url SITE_URL] [ENVIRONMENT_DIR [PORT]]

Options:
  --address=IP            Address to listen on (Linux-only) [default: 127.0.0.1]
  -i --image-only         Create the environment but don't start containers
  -n --no-sysadmin        Don't prompt for an initial sysadmin user account
  -s --site=NAME          Pick a site to initialize [default: primary]
  --site-url SITE_URL     The site_url to use in API responses (e.g. http://example.org:{port}/)
  --syslog                Log to the syslog

ENVIRONMENT_DIR is an existing datacats environment directory. Defaults to '.'
"""
    environment_dir = opts['ENVIRONMENT_DIR']
    port = opts['PORT']
    address = opts['--address']
    start_web = not opts['--image-only']
    create_sysadmin = not opts['--no-sysadmin']
    site_name = opts['--site']
    site_url = opts['--site-url']

    environment_dir = abspath(environment_dir or '.')
    log_syslog = opts['--syslog']

    environment = Environment.load(environment_dir, site_name)
    environment.address = address
    if port:
        environment.port = int(port)
    if site_url:
        environment.site_url = site_url

    try:
        if environment.sites and site_name in environment.sites:
            raise DatacatsError('Site named {0} already exists.'
                                .format(site_name))
        # There are a couple of steps we can/must skip if we're making a sub-site only
        making_full_environment = not environment.data_exists()

        if not quiet:
            write('Creating environment {0}/{1} '
                  'from existing environment directory "{0}"'
                  .format(environment.name, environment.site_name))
        steps = [
            lambda: environment.create_directories(create_project_dir=False)] + ([
             environment.save,
             environment.create_virtualenv
             ] if making_full_environment else []) + [
                 environment.save_site,
                 environment.start_supporting_containers,
                 environment.fix_storage_permissions,
            ]

        for fn in steps:
            fn()
            if not quiet:
                write('.')
        if not quiet:
            write('\n')
    except:
        if not quiet:
            print
        raise

    return finish_init(environment, start_web, create_sysadmin, address,
                       log_syslog=log_syslog, do_install=not no_install,
                       quiet=quiet, site_url=site_url)
