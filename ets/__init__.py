# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Toolkit for environment management and continuous integration.

The :mod:`ets` package provides utilities for environment management
and building continuous integration infrastructure that is used by the
various Enthought Tool Suite projects.

It is designed to be installed in a "bootstrap" environment, such as a
developers' everyday Python environment.  Once installed it is designed
provide a toolkit for writing continuous integration and deployment
scripts, and provides a toolkit for doing common operations, such as
creating venv or EDM environments, installing modules, running tests,
linting, and generating documentation.

It could potentially also be used to generate demo environments and run
demo scripts to highlight the capabilities of various libraries.

For an example of usage, see the ``etstool.py`` script in the main ets
directory.
"""
