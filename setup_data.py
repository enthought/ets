requirements = [
    ('apptools', '4.2.1'),
    ('blockcanvas', '4.0.3'),
    ('chaco', '4.4.1'),
    ('codetools', '4.2.0'),
    ('enable', '4.4.1'),
    ('enaml', '0.9.5'),
    ('encore', '0.5.1'),
    ('envisage', '4.4.0'),
    ('etsdevtools', '4.0.2'),
    ('etsproxy', '0.1.2'),
    ('graphcanvas', '4.0.2'),
    ('mayavi', '4.3.1'),
    ('pyface', '4.4.0'),
    ('scimath', '4.1.2'),
    ('traits', '4.5.0'),
    ('traitsui', '4.4.0'),
]

INFO = {
    'name': 'ets',
    'version': '4.4.2',
    'install_requires': ['%s >= %s.dev' % nv for nv in requirements],
}
