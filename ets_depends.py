"""
Extract dependency info from ETS setup files.
Should be run from the ETS root directory, which contains the
directories for each ETS package.
"""
import os
from ets import ets_package_names
INDENT = '  '

for pkg_name in ets_package_names.split():
    setup_data = dict(__name__='', __file__='setup_data.py')
    try:
        execfile(os.path.join(pkg_name,'setup_data.py'), setup_data)
        INFO = setup_data['INFO']
        print '%s %s' % (INFO['name'], INFO['version'])
        print INDENT + 'ETS installation dependencies:'
        for item in INFO['install_requires']:
            print INDENT*2 + str(item)
        if 'extras_require' not in INFO:
            continue
        print INDENT + 'Other dependencies:'
        for (key,value) in INFO['extras_require'].items():
            if value:
                print '%s%s' % ( INDENT*2, key)
                try:
                    for sub_item in value:
                        print INDENT*3,sub_item
                except TypeError:
                    print INDENT*3,value
    except (IOError,), ermsg:
        print pkg_name
        print INDENT + str(ermsg)
