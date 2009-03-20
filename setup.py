#!/usr/bin/env python
#
# Copyright (c) 2008-2009 by Enthought, Inc.
# All rights reserved.


"""
The Enthought Tool Suite meta-project.

The Enthought Tool Suite (ETS) is a collection of components developed by
Enthought and our partners, which we use every day to construct custom
scientific applications.

This project is a "meta-project wrapper" that bundles up all the other projects
in ETS.
"""


from setuptools import setup, find_packages


# Pull the description values for the setup keywords from our file docstring.
DOCLINES = __doc__.split("\n")


# Function to convert simple ETS component names and versions to a requirements
# spec that works for both development builds and stable builds.
def build_reqs(list):
    return ['%s >=%s.dev, <=%s' % (p, v, v) for p,v in list]

# Declare the ETS component versions
install_requires = build_reqs([
    ('AppTools', '3.2.0'),
    ('BlockCanvas', '3.0.2'),
    ('Chaco', '3.1.0'),
    ('CodeTools', '3.0.2'),
    ('Enable', '3.1.0'),
    ('EnthoughtBase', '3.0.2'),
    ('EnvisageCore', '3.1.0'),
    ('EnvisagePlugins', '3.1.0'),
    ('ETSDevTools', '3.0.2'),
    ('ETSProjectTools', '0.5.0'),
    ('Mayavi', '3.2.0'),
    ('SciMath', '3.0.3'),
    ('SetupDocs', '1.0.2'),
    ('Traits', '3.1.0'),
    ('TraitsBackendQt', '3.1.0'),
    ('TraitsBackendWX', '3.1.0'),
    ('TraitsGUI', '3.0.4'),
    ])


# The actual setup call.
setup(
    author = 'Enthought, Inc.',
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
            'ETSProjectTools[nonets]',
            'Mayavi[nonets]',
            'SciMath[nonets]',
            'SetupDocs[nonets]',
            'Traits[nonets]',
            'TraitsBackendQt[nonets]',
            'TraitsBackendWX[nonets]',
            'TraitsGUI[nonets]'
            ],
        },
    include_package_data = True,
    install_requires = install_requires,
    license = 'BSD',
    long_description = '\n'.join(DOCLINES[3:]),
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    name = 'ETS',
    packages = '',
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    tests_require = [
        'nose >= 0.9',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/projects/tool-suite.php',
    version = '3.2.0',
    zip_safe = True,
    )

