# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Code for working with Python environments. """

from abc import ABC, abstractmethod
import os
import shutil

from .util import execute, do_in_existingdir, do_in_tempdir, update_os_environ


class Environment(ABC):
    """ Abstract class for environments.

    Different concrete subclasses will use a particular environment manager,
    like EDM or venv, to manage the state of the environment and execute
    commands and operations within it.

    Attributes
    ----------
    manager : str
        A human-readable name of the environment manager.
    environment : str
        The name of the environment.
    runtime : str
        The Python runtime version for the environment.
    """

    def __init__(self, environment, runtime):
        self.environment = environment
        self.runtime = runtime

    @abstractmethod
    def create(self, force=True):
        """ Create the environment.

        Parameters
        ----------
        force : bool
            If force is True, any existing environment with the same name
            will be removed.
        """
        raise NotImplementedError()

    @abstractmethod
    def clean(self):
        """ Clean-up the environment.

        This attempts to destroy the environment, if possible.
        """
        raise NotImplementedError()

    @abstractmethod
    def install(self, packages):
        """ Install packages.

        The default implementation uses pip to install.

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
        packages = [
            package['pip'] for package in packages
            if 'pip' in package
        ]
        self.pip_install(packages)

    def install_source(self, path='.', editable=False):
        """ Install a package from a source directory.

        Parameters
        ----------
        path : pathlike
            The path to the source directory.
        editable : bool
            Whether to perform an editable installation, so changes to the
            source are automatically picked up.
        """
        if editable:
            self.invoke_module(
                'pip', 'install', '--no-dependencies', '--editable', str(path)
            )
        else:
            self.invoke_module(
                'pip', 'install', '--no-dependencies', str(path)
            )

    @abstractmethod
    def uninstall(self, packages):
        """ Uninstall packages.

        The default implementation uses pip to uninstall.

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
        # default implementation uses pip to uninstall
        packages = [
            package['pip'] for package in packages
            if 'pip' in package
        ]
        self.pip_uninstall(packages)

    @abstractmethod
    def invoke_module(self, module, *args):
        """ Run a module using ``python -m`` within the environment.

        Parameters
        ----------
        module : str
            The name of the module to run.
        *args
            Additional arguments for the module.
        """
        raise NotImplementedError()

    @abstractmethod
    def invoke_script(self, script, *args):
        """ Run a script within the environment.

        Parameters
        ----------
        script : str
            The name of the script to run.
        *args
            Additional arguments for the script.
        """
        raise NotImplementedError()

    def pip_install(self, packages):
        """ Install packages using pip.

        This should work in any well-behaved environment.

        Parameters
        ----------
        packages : list of str
            List of package specifications to install.
        """
        self.invoke_module('pip', 'install', *packages)

    def pip_uninstall(self, packages):
        """ Uninstall packages using pip.

        This should work in any well-behaved environment.

        Parameters
        ----------
        packages : list of str
            List of package specifications to uninstall.
        """
        self.invoke_module('pip', 'uninstall', '-y', *packages)

    def run_tests(self, module, discover=True, verbose=True,
                  coveragerc='.coveragerc'):
        """ Run unit tests with coverage.

        Parameters
        ----------
        module : str
            The name of the module to perform test discovery on.
        discover : bool
            Whether to perform test discovery.
        verbose : bool
            Whether to use verbose unittest output.
        coveragerc : pathlike
            The location of the .coveragerc file for generating
            code coverage metrics.
        """
        environ = {}
        environ["PYTHONUNBUFFERED"] = "1"

        args = 'run -p -m -- unittest'.split()
        if discover:
            args.append('discover')
        if verbose:
            args.append('--verbose')
        args.append(module)
        with do_in_tempdir(files=[coveragerc],
                           capture_files=["./.coverage.*"]):
            with update_os_environ(environ):
                self.invoke_module('coverage', *args)
                self.invoke_module('coverage', 'combine')
                self.invoke_module('coverage', 'report', '-m')

    def flake8(self, dir):
        """ Run flake8 over the codebase.

        Parameters
        ----------
        dir : pathlike
            The directory containing the source code.
        """
        self.invoke_module('flake8', str(dir))

    def mypy(self, dir):
        """ Run mypy over the codebase.

        Parameters
        ----------
        dir : pathlike
            The directory containing the source code.
        """
        self.invoke_module('mypy', str(dir))

    def bandit(self, dir, level=2):
        """ Run bandit over the codebase.

        Parameters
        ----------
        dir : pathlike
            The directory containing the source code.
        """
        level = '-' + 'l'*level
        self.invoke_module('bandit', level, '-r', str(dir))

    def pydocstyle(self, dir, ):
        """ Run pydocstyle over the codebase.

        Parameters
        ----------
        dir : pathlike
            The directory containing the source code.
        """
        self.invoke_module('pydocstyle', str(dir))

    def apidoc(self, source_dir, api_dir, exclude=[]):
        """ Auto-generate API documentation.

        Parameters
        ----------
        source_dir : pathlike
            The directory containing the source code.
        api_dir : pathlike
            The directory containing the api documentation.
        exclude : list of patterns
            List of source file patterns to exclude from the API
            documentation.
        """
        if os.path.exists(api_dir):
            shutil.rmtree(api_dir)
        os.makedirs(api_dir)
        self.invoke_script(
            'sphinx-apidoc', "-e", "-M", "-o", str(api_dir), str(source_dir),
            *exclude
        )

    def build_docs(self, docs_dir='docs', error_on_warn=False):
        """ Build sphinx documentation.

        Parameters
        ----------
        docs_dir : pathlike
            The top-level directory containing the documentation.
        error_on_warn : bool
            Whether to raise an error if there are any warnings generated
            by Sphinx.
        """
        args = ["-b", "html"]
        if error_on_warn:
            args.append("-W")
        args += ["-d", "build/doctrees", "source", "build/html"]

        with do_in_existingdir(docs_dir):
            self.invoke_script('sphinx-build', *args)

    def execute(self, commands):
        """ Execute a series of commands.

        This is a wrapper around the :func:`ets.utils.execute` function which
        uses the environment as a namespace for parameter substitution in
        arguments.

        Parameters
        ----------
        commands : list of list of str
            A list of commands, each command a list of strings suitable for
            use with :func:`subprocess.call` and related functions.

        Raises
        ------
        SystemExit
            If any command fails, :func:`sys.exit` will be called with error
            code 1.
        """
        parameters = self.__dict__
        execute(commands, parameters)
