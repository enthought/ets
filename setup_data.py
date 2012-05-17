requirements = [
    ('apptools', '4.1.0'),
    ('blockcanvas', '4.0.1'),
    ('chaco', '4.2.0'),
    ('codetools', '4.0.0'),
    ('enable', '4.2.0'),
    ('enaml', '0.2.0'),
    ('encore', '0.2.0'),
    ('envisage', '4.2.0'),
    ('etsdevtools', '4.0.0'),
    ('etsproxy', '0.1.1'),
    ('graphcanvas', '4.0.0'),
    ('mayavi', '4.2.0'),
    ('pyface', '4.2.0'),
    ('scimath', '4.1.0'),
    ('traits', '4.2.0'),
    ('traitsui', '4.2.0'),
]

INFO = {
    'name': 'ets',
    'version': '4.2.1',
    'install_requires': ['%s >= %s.dev' % nv for nv in requirements],
}
