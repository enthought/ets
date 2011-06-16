requirements = [
    ('apptools', '4.0.0'),
    ('blockcanvas', '4.0.0'),
    ('chaco', '4.0.0'),
    ('codetools', '4.0.0'),
    ('enable', '4.0.0'),
    ('envisage', '4.0.0'),
    ('etsdevtools', '4.0.0'),
    ('etsproxy', '0.1.0'),
    ('graphcanvas', '4.0.0'),
    ('mayavi', '4.0.0'),
    ('pyface', '4.0.0'),
    ('scimath', '4.0.0'),
    ('traits', '4.0.0'),
    ('traitsui', '4.0.0'),
]

INFO = {
    'name': 'ets',
    'version': '4.0.0',
    'install_requires': ['%s >= %s.dev' % nv for nv in requirements],
}
