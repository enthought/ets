#!/usr/bin/env python
#
# Copyright (c) 2008-2010 by Enthought, Inc.
# All rights reserved.

"""
The Enthought Tool Suite meta-project.

The Enthought Tool Suite (ETS) is a collection of components developed by
Enthought and our partners, which we use every day to construct custom
scientific applications.

This project is a "meta-project wrapper" that bundles up all the other projects
in ETS.
"""

from setuptools import setup


# Pull the description values for the setup keywords from our file docstring.
DOCLINES = __doc__.split("\n")


# Function to convert simple ETS component names and versions to a requirements
# spec that works for both development builds and stable builds.
def build_reqs(list):
    return ['%s >=%s.dev, <=%s' % (p, v, v) for p,v in list]

# Declare the ETS component versions
install_requires = build_reqs([
    ('AppTools', '3.4.0'),
    ('BlockCanvas', '3.2.0'),
    ('Chaco', '3.3.2'),
    ('CodeTools', '3.1.2'),
    ('Enable', '3.3.2'),
    ('EnthoughtBase', '3.0.6'),
    ('EnvisageCore', '3.1.3'),
    ('EnvisagePlugins', '3.1.3'),
    ('ETSDevTools', '3.1.0'),
    ('Mayavi', '3.4.0'),
    ('SciMath', '3.0.5'),
    ('SetupDocs', '1.0.5'),
    ('Traits', '3.5.0'),
    ('TraitsBackendQt', '3.5.0'),
    ('TraitsBackendWX', '3.5.0'),
    ('TraitsGUI', '3.5.0'),
])

INFO = {}
INFO['version'] = '3.5.1'

# The actual setup call.
setup(
    name = 'ETS',
    version = INFO['version'],
    author = 'Enthought, Inc.',
    download_url = ('http://www.enthought.com/repo/ETS/ETS-%s.tar.gz' %
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
    extras_require = {
        # Allow users to decide if they install ETS without external
        # dependencies
        'nonets': [
            'AppTools[nonets]',
            'BlockCanvas[nonets]',
            'Chaco[nonets]',
            'CodeTools[nonets]',
            'Enable[nonets]',
            'EnthoughtBase[nonets]',
            'EnvisageCore[nonets]',
            'EnvisagePlugins[nonets]',
            'ETSDevTools[nonets]',
            'Mayavi[nonets]',
            'SciMath[nonets]',
            'SetupDocs[nonets]',
            'Traits[nonets]',
            'TraitsBackendQt[nonets]',
            'TraitsBackendWX[nonets]',
            'TraitsGUI[nonets]'
            ],
        },
    install_requires = install_requires,
    license = 'BSD',
    long_description = '\n'.join(DOCLINES[3:]),
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    py_modules = ["ets"],
    entry_points = dict(console_scripts=["ets = ets:main"]),
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    url = 'http://code.enthought.com/projects/tool-suite.php',
)
