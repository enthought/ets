from setuptools import setup, find_packages


# Function to convert simple ETS component names and versions to a requirements
# spec that works for both development builds and stable builds.
def build_reqs(list):
    return ['%s >=%s.dev, <=%s' % (p, v, v) for p,v in list]

# Declare the ETS component versions
install_requires = build_reqs([
    ('AppTools', '3.0.0b1'),
    ('BlockCanvas', '3.0.0b1'),
    ('Chaco', '3.0.0b1'),
    ('DevTools', '3.0.0b1'),
    ('Enable', '3.0.0b1'),
    ('Enstaller', '2.2.0b4'),
    ('EnstallerGUI', '2.2.0b4'),
    ('EnthoughtBase', '3.0.0b1'),
    ('EnvisageCore', '3.0.0b1'),
    ('EnvisagePlugins', '3.0.0b1'),
    ('ETSProjectTools', '0.3.0a1'),
    ('Mayavi', '3.0.0a1'),
    ('SciMath', '3.0.0b1'),
    ('Traits', '3.0.0b1'),
    ('TraitsBackendQt', '3.0.0b1'),
    ('TraitsBackendWX', '3.0.0b1'),
    ('TraitsGUI', '3.0.0b1'),
    ])


setup(
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        ],
    description = 'Enthought Tool Suite Library',
    extras_require = {
        # Allow users to decide if they install ETS without external
        # dependencies
        'nonets': [
            'AppTools[nonets]',
            'BlockCanvas[nonets]',
            'Chaco[nonets]',
            'DevTools[nonets]',
            'Enable[nonets]',
            'Enstaller[nonets]',
            'EnstallerGUI[nonets]',
            'EnthoughtBase[nonets]',
            'EnvisageCore[nonets]',
            'EnvisagePlugins[nonets]',
            'ETSProjectTools[nonets]',
            'Mayavi[nonets]',
            'SciMath[nonets]',
            'Traits[nonets]',
            'TraitsBackendQt[nonets]',
            'TraitsBackendWX[nonets]',
            'TraitsGUI[nonets]'
            ],
        },
    include_package_data = True,
    install_requires = install_requires,
    license = 'BSD',
    name = 'ETS',
    packages = '',
    tests_require = [
        'nose >= 0.9',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/ets',
    version = '3.0.0b1',
    zip_safe = True,
    )

