# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Helpers for creating click-based scripts.
"""

import sys

import click

from .edm import EDM
from .venv import Venv


#: The runtimes that we generally support.  Modify this in-place to
#: change what might be supported for a particular script.
supported_runtimes = ["3.5", "3.6", "3.7", "3.8", "3.9"]

#: The default runtime version is the current Python version.
default_runtime = '{}.{}'.format(*sys.version_info[:2])


environment_manager = {
    'venv': Venv,
    'edm': EDM,
}


def create_environment_manager(ctx, param, value):
    """ Create an environment object. """
    environment = ctx.params.get('environment')
    runtime = ctx.params.get('runtime')
    if environment is None:
        environment = "ets-test-{runtime}".format(runtime=runtime)
        ctx.params['environment'] = environment

    cls = environment_manager[value]
    return cls(environment, runtime)


runtime_option = click.option(
    "--runtime",
    default=default_runtime,
    type=click.Choice(supported_runtimes),
    show_default=True,
    help="Python runtime version for the development environment",
)
environment_option = click.option(
    "--environment",
    default=None,
    help="Name of the environment to install",
)
environment_manager_option = click.option(
    "--environment-manager",
    default='venv',
    help="Environment management tool to use",
    callback=create_environment_manager
)

editable_option = click.option(
    "--editable/--not-editable",
    default=False,
    help="Install main package in 'editable' mode?  [default: --not-editable]",
)
verbose_option = click.option(
    "--verbose/--quiet",
    default=True,
    help="Run tests in verbose mode? [default: --verbose]",
)

docs_option = click.option(
    "--docs/--no-docs",
    default=True,
    help="Install documentation dependencies.",
)

tests_option = click.option(
    "--tests/--no-tests",
    default=True,
    help="Install test dependencies.",
)
