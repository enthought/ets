#!/usr/bin/env python
#
# Copyright (c) 2008-2011 by Enthought, Inc.
# All rights reserved.

"""
The Enthought Tool Suite meta-project.

The Enthought Tool Suite (ETS) is a collection of components developed by
Enthought and our partners, which we use every day to construct custom
scientific applications.

This project is a "meta-project wrapper" that bundles up all the other projects
in ETS.
"""

import sys
from setuptools import setup


# Pull the description values for the setup keywords from our file docstring.
DOCLINES = __doc__.split("\n")

setup_data = dict(__name__='', __file__='setup_data.py')
execfile('setup_data.py', setup_data)
INFO = setup_data['INFO']

if 'develop' in sys.argv:
    INFO['install_requires'] = []

# The actual setup call.
setup(
    name = 'ETS',
    version = INFO['version'],
    author = 'Enthought, Inc.',
    download_url = ('http://www.enthought.com/repo/ets/ETS-%s.tar.gz' %
                    INFO['version']),
    author_email = 'info@enthought.com',
    classifiers = [c.strip() for c in """\
        Development Status :: 4 - Beta
        Intended Audience :: Developers
        Intended Audience :: Science/Research
        License :: OSI Approved :: BSD License
        Operating System :: MacOS
        Operating System :: Microsoft :: Windows
        Operating System :: OS Independent
        Operating System :: POSIX
        Operating System :: Unix
        Programming Language :: Python
        Topic :: Scientific/Engineering
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        """.splitlines() if len(c.strip()) > 0],
    description = DOCLINES[1],
    install_requires = INFO['install_requires'],
    license = 'BSD',
    long_description = '\n'.join(DOCLINES[3:]),
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    py_modules = ["ets"],
    entry_points = dict(console_scripts=["ets = ets:main"]),
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    url = 'http://code.enthought.com/projects/tool-suite.php',
)
