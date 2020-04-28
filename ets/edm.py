# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Code for working with EDM-based Python environments. """

import os
import shutil
import sys

import click

from .environment import Environment

#: Command templates for operations.
CREATE_COMMAND = "{edm} environments create {environment} --version={runtime}"
CLEAN_COMMAND = "{edm} environments remove {environment} --purge -y"
INSTALL_COMMAND = "{edm} install -e {environment} -y"
REMOVE_COMMAND = "{edm} plumbing remove-package --environment {environment} --force"  # noqa: E501
INVOKE_MODULE = "{edm} run -- python -m"
INVOKE_SCRIPT = "{edm} run --"


class EDM(Environment):
    """ An EDM-based Python environment.

    Attributes
    ----------
    manager : str
        A human-readable name of the environment manager.
    environment : str
        The name of the environment.
    runtime : str
        The Python runtime version for the environment.
    edm : str
        The location of the EDM executable.
    """

    #: The user-facing name of the environment manager.
    manager = "edm"

    def __init__(self, environment, runtime):
        super().__init__(environment, runtime)
        self.edm = locate_edm()

    def create(self, force=True):
        """ Create the environment.

        Parameters
        ----------
        force : bool
            If force is True, any existing environment with the same name
            will be removed.
        """
        create_command = CREATE_COMMAND.split()
        if force:
            create_command.append("--force")
        self.execute([create_command])

    def clean(self):
        """ Clean-up the environment.

        This attempts to destroy the environment, if possible.
        """
        remove_command = CLEAN_COMMAND.split()
        self.execute([remove_command])

    def install(self, packages):
        """ Install packages.

        This uses edm where the package is available for edm, otherwise
        trying pip.

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
        edm_packages = [
            package['edm'] for package in packages
            if 'edm' in package
        ]
        if edm_packages:
            install_command = INSTALL_COMMAND.split() + edm_packages
            self.execute([install_command])

        other_packages = [
            package['pip'] for package in packages
            if 'edm' not in package
        ]
        if other_packages:
            self.pip_install(other_packages)

    def uninstall(self, packages):
        """ Uninstall packages.

        If the package is known to EDM, this attempts to uninstall it,
        otherwise it tries using pip.

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
        edm_packages = [
            package['edm'] for package in packages
            if 'edm' in package
        ]
        if edm_packages:
            remove_command = REMOVE_COMMAND + edm_packages
            self.execute([remove_command])

        other_packages = [
            package['pip'] for package in packages
            if 'edm' not in package
        ]
        if other_packages:
            self.pip_uninstall(other_packages)

    def invoke_module(self, module, *args):
        """ Run a module using ``python -m`` within the environment.

        Parameters
        ----------
        module : str
            The name of the module to run.
        *args
            Additional arguments for the module.
        """
        command = INVOKE_MODULE.split() + [module] + list(args)
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
        command = INVOKE_SCRIPT.split() + [script] + list(args)
        self.execute([command])


def locate_edm():
    """ Locate an EDM executable if it exists, else raise an exception.

    Returns the first EDM executable found on the path. On Windows, if that
    executable turns out to be the "edm.bat" batch file, replaces it with the
    executable that it wraps: the batch file adds another level of command-line
    mangling that interferes with things like specifying version restrictions.

    Returns
    -------
    edm : str
        Path to the EDM executable to use.

    Raises
    ------
    click.ClickException
        If no EDM executable is found in the path.
    """
    edm = shutil.which('edm')
    if edm is None:
        raise click.ClickException(
            "This script requires EDM, but no EDM executable was found."
        )

    # Resolve edm.bat on Windows.
    if sys.platform == "win32" and os.path.basename(edm) == "edm.bat":
        edm = os.path.join(os.path.dirname(edm), "embedded", "edm.exe")

    return edm
