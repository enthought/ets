# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import sys
from setuptools import setup, find_packages


setup_data = {'requirements': []}
exec(open('setup_data.py').read(), setup_data)
INFO = setup_data['INFO']

if 'develop' in sys.argv:
    INFO['install_requires'] = []

# The actual setup call.
setup(
    version=INFO['version'],
    install_requires=INFO['install_requires'],
    packages=find_packages(),
    entry_points={
        # 'console_scripts': [
        #     "ets = ets.scripts.ets:main",
        #     "ets-docs = ets.scripts.ets_docs:main",
        # ],
        "flake8.extension": [
            "H = ets.copyright_header:CopyrightHeaderExtension",
        ],
    },
#    platforms=["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
)
