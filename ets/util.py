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
Utility methods for code execution and directory management.
"""

from contextlib import contextmanager
import glob
import os
from shutil import copy, rmtree
import subprocess
import sys
from tempfile import mkdtemp

import click


@contextmanager
def do_in_tempdir(files=(), capture_files=()):
    """ Create a temporary directory, cleaning up after done.

    Creates the temporary directory, and changes into it.  On exit returns to
    original directory and removes temporary dir.

    Parameters
    ----------
    files : sequence of filenames
        Files to be copied across to temporary directory.
    capture_files : sequence of filenames
        Files to be copied back from temporary directory.
    """
    path = mkdtemp()
    old_path = os.getcwd()

    # send across any files we need
    for filepath in files:
        click.echo("copying file to tempdir: {}".format(filepath))
        copy(filepath, path)

    os.chdir(path)
    try:
        yield path
        # retrieve any result files we want
        for pattern in capture_files:
            for filepath in glob.iglob(pattern):
                click.echo("copying file back: {}".format(filepath))
                copy(filepath, old_path)
    finally:
        os.chdir(old_path)
        rmtree(path)


@contextmanager
def do_in_existingdir(path):
    """ Change directory to an existing directory, change back when done.

    Parameters
    ----------
    path : str
        Path of the directory to be changed into.
    """
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(old_path)


@contextmanager
def update_os_environ(environ):
    """ Temporarily set environment variables.

    This will overwrite existing environment variable values, or
    create new environment variables as needed.  The original state
    will be restored when the context manager exits.

    Parameters
    ----------
    environ : dict
        Dictionary of new environment variables to set.
    """
    old_values = {
        key: os.environ[key]
        for key in environ
        if key in os.environ
    }
    os.environ.update(environ)
    try:
        yield
    finally:
        for key in set(environ) - set(old_values):
            del os.environ[key]
        os.environ.update(old_values)


def execute(commands, parameters):
    """ Execute a sequence of commands, substituting parameter values.

    Each command is a list of strings, each string being an argument of the
    command.  Python format-style substitution is performed on each argument
    prior to the command being executed.

    Parameters
    ----------
    commands : list of list of str
        A list of commands, each command being a list of strings forming the
        parts of a command to be run by :func:`subprocess.call` or similar.
        functions.  The strings may contain Python keyword format-style
        formatting for parameter substitution.
    parameters : dict
        A mapping of parameter names to values for substitution into command
        arguments.

    Raises
    ------
    SystemExit
        If the subprocess has an error, the function raises :func:`sys.exit`
        with error code 1.
    """
    for command in commands:
        command_list = [arg.format(**parameters) for arg in command]
        click.echo("[EXECUTING] {}".format(' '.join(command_list)))
        try:
            subprocess.check_call(command_list)  # nosec
        except subprocess.CalledProcessError as exc:
            print(exc)
            sys.exit(1)
