requirements = [
#     ('apptools', '4.2.1'),
#     ('blockcanvas', '4.0.3'),
#     ('chaco', '4.5.0'),
#     ('codetools', '4.2.0'),
#     ('enable', '4.4.1'),
#     ('encore', '0.6.0'),
#     ('envisage', '4.4.0'),
#     ('etsdevtools', '4.0.2'),
#     ('etsproxy', '0.1.2'),
#     ('graphcanvas', '4.0.2'),
#     ('mayavi', '4.3.1'),
#     ('pyface', '4.4.0'),
#     ('scimath', '4.1.2'),
#     ('traits', '4.5.0'),
#     ('traitsui', '4.4.0'),
]

INFO = {
    'name': 'ets',
    'version': '5.0.0',
    'install_requires': ['click'] + ['%s >= %s.dev' % nv for nv in requirements],
}
