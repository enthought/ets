from setuptools import setup, find_packages


# Function to convert simple ETS component names and versions to a requirements
# spec that works for both development builds and stable builds.
def build_reqs(list):
    return ['%s >=%s.dev, <=%s' % (p, v, v) for p,v in list]

# Declare the ETS component versions
install_requires = build_reqs([
    ("enthought.chaco2", "3.0a1"),
    ('enthought.debug', '2.1.0a1'),
    ("enthought.enable2", "3.0a1"),
#    ('enthought.enstaller', '2.2.0b3'), -- removed, at Rick's recommendation, due to bugs with running enstaller
#    ('enthought.enstaller.gui', '2.2.0b3'), -- removed, at Rick's recommendation, due to bugs with running enstaller
    ("enthought.envisage", "3.0a1"),
    ('enthought.envisage.ui.workbench', '3.0a1'),
    ("enthought.etsconfig", "2.1.0a1"),
    ("enthought.gotcha", "2.1.0a1"),
    ("enthought.greenlet", "2.1.0a1"),
    ("enthought.guitest", "2.1.0a1"),
    ("enthought.help", "3.0a1"),
    ('enthought.interpolate', '2.1.0a1'),
    ("enthought.io", "2.1.0a1"),
    ("enthought.kiva", "3.0a1"),
    ("enthought.logger", "3.0a1"),
    ("enthought.mathematics", "2.1.0a1"),
    ("enthought.mayavi", "2.0.2a1"),
    ("enthought.model", "3.0a1"),
    ("enthought.naming", "3.0a1"),
    ("enthought.numerical_modeling", "3.0a1"),
    ("enthought.persistence", "2.1.0a1"),
    ('enthought.plugins.chaco', '1.10.0a1'),
    ('enthought.plugins.debug', '2.1.0a1'),
    ("enthought.plugins.python_shell", "3.0a1"),
    ("enthought.plugins.refresh_code", "2.1.0a1"),
    ("enthought.plugins.text_editor", "3.0a1"),
    ("enthought.pyface", "3.0a1"),
    ('enthought.pyface.ui.qt4', '3.0a1'),
    ('enthought.pyface.ui.wx', '3.0a1'),
    ("enthought.python", "2.1.0a1"),
    ("enthought.setuptools", "0.3.0a1"),
    ("enthought.sweet_pickle", "2.1.0a1"),
    ("enthought.testing", "2.1.0a1"),
    ("enthought.traits", "3.0.0b1"),
    ("enthought.traits.ui.wx", "3.0.0b1"),
    ("enthought.tvtk", "3.0a1"),
    ("enthought.type_manager", "2.1.0a1"),
    ('enthought.undo', '1.0a1'),
    ("enthought.units", "3.0a1"),
    ("enthought.util", "3.0a1"),
    ])
print 'install_requires:\n\t%s' % '\n\t'.join(install_requires)


setup(
    name = 'ets',
    version = '3.0a1',
    description = 'Enthought Tool Suite Library',
    author = 'Enthought, Inc',
    author_email = 'info@enthought.com',
    url = 'http://code.enthought.com/ets',
    license = 'BSD',
    zip_safe = True,
    packages = '',
    include_package_data = True,
    install_requires = install_requires,
    extras_require = {
        # Allow users to decide if they install ETS without external
        # dependencies
        'nonets': [
            'enthought.chaco2[nonets]',
            'enthought.enable2[nonets]',
            'enthought.kiva[nonets]',
            'enthought.numerical_modeling[nonets]',
            'enthought.units[nonets]',
            ],
        },
    )

