# Copyright (c) 2008-2011 by Enthought, Inc.
# All rights reserved.

import sys
from setuptools import setup


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
    description = 'Enthought Tool Suite meta-project',
    long_description = open('README.rst').read(),
    install_requires = INFO['install_requires'],
    license = 'BSD',
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    py_modules = ["ets", "ets_docs"],
    entry_points = dict(console_scripts=[
            "ets = ets:main",
            "ets-docs = ets_docs:main",
    ]),
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    url = 'http://code.enthought.com/projects/tool-suite.php',
)
