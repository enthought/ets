# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Code for working with venv virtual environments. """

import os
from pathlib import Path
import sys
import shutil

import click

from .environment import Environment


#: virtualenv wrapper default, good enough for a default
default_venv_path = Path('~/.virtualenvs')


def get_venv_path():
    """ Heuristics for the place to locate virtual environments.

    This method looks for (in order of priority):

    - an ``ETS_VENV_PATH`` enviornment variable
    - a ``WORKON_HOME`` environment variable

    If neither exits, it uses ``~/.virtualenvs``.  This can be overridden
    by changing the module-level :obj:`default_venv_path` value.

    Returns
    -------
    path : Path
        The best-guess at the location of virtual environments.
    """
    # virtualenv wrapper and other tools use 'WORKON_HOME'
    virtualenv_wrapper_path = os.environ.get('WORKON_HOME', default_venv_path)

    # ETS-specific environment variable that overrides the above
    venv_path = os.environ.get('ETS_VENV_PATH', virtualenv_wrapper_path)

    return Path(venv_path).expanduser().resolve()


class Venv(Environment):
    """ A venv-based virtual environment.

    Attributes
    ----------
    manager : str
        A human-readable name of the environment manager.
    environment : str
        The name of the environment.
    runtime : str
        The Python runtime version for the environment.
    base_path : Path
        The root of the virtual environment in the filesystem.
    script_dir : Path
        The path to the script directory within the virtual environment.
    python : Path
        The path to the python executable within the virtual environment.
    bootstrap_python : Path
        The path to a python executable that can be used to create the
        environment.
    """

    #: The user-facing name of the environment manager.
    manager = "venv"

    def __init__(self, environment, runtime):
        super().__init__(environment, runtime)
        base_path = Path(environment)
        if not base_path.is_absolute():
            base_path = get_venv_path().joinpath(base_path)

        self.base_path = base_path.resolve()

        if sys.platform == "win32":
            self.script_dir = self.base_path / "Scripts"
        else:
            self.script_dir = self.base_path / "bin"

        self.python = self.script_dir / "python"
        self.bootstrap_python = get_python(runtime)

    def create(self, force=True):
        """ Create the environment.

        Parameters
        ----------
        force : bool
            If force is True, any existing environment with the same name
            will be removed.
        """
        install_command = "{bootstrap_python} -m venv {base_path}".split()
        if force:
            install_command.append("--clear")
        self.execute([install_command])
        self.invoke_module('pip', 'install', '--upgrade', 'pip')

    def clean(self):
        """ Clean-up the environment.

        This attempts to destroy the environment, if possible.

        Note
        ----
        On windows this may fail if any file in the environment is open.
        """
        # XXX may fail on Windows if files in environment are in use
        shutil.rmtree(self.base_path)

    def install(self, packages):
        """ Install packages.

        This class uses pip to install packages.

        Parameters
        ----------
        packages : list of package dicts
            List of package specifications to install.  A package
            specification is a dictionary with items of the form::

                manager: specification

            where manager is the name of the manager and specification is
            a string which specifies a package in a way that the manager
            understands.
        """
        super().install(packages)

    def uninstall(self, packages):
        """ Uninstall packages.

        This class uses pip to uninstall packages.

        Parameters
        ----------
        packages : list of package dicts
            List of package specifications to uninstall.  A package
            specification is a dictionary with items of the form::

                manager: specification

            where manager is the name of the manager and specification is
            a string which specifies a package in a way that the manager
            understands.
        """
        super().uninstall(packages)

    def invoke_module(self, module, *args):
        """ Run a module using ``python -m`` within the environment.

        Parameters
        ----------
        module : str
            The name of the module to run.
        *args
            Additional arguments for the module.
        """
        command = ["{python}", "-m", module] + list(args)
        self.execute([command])

    def invoke_script(self, script, *args):
        """ Run a script within the environment.

        Parameters
        ----------
        script : str
            The name of the script to run.
        *args
            Additional arguments for the script.
        """
        path = self.script_dir / script
        command = [str(path)] + list(args)
        self.execute([command])


def get_python(runtime):
    """ Find the requested Python version to run the venv module.
    """
    python = shutil.which('python'+runtime)
    if python is None:
        msg = "This script requires {python}, but no {python} executable was found."  # noqa
        raise click.ClickException(
            msg.format(python="Python "+runtime)
        )
    return python
