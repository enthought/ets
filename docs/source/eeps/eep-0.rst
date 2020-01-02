=================================
EEP 0: EEP Purpose and Guidelines
=================================

:Author: Corran Webster
:Status: Active
:Type: Informational
:Content-Type: text/x-rst
:Created: 2020-01-02
:Post-History: 2020-01-02


What is an EEP?
===============

An EEP is an ETS Enhancement Proposal, similar in pupose and conventions
to Python Enhancement Proposals [1]_.  At present they are intended to be
less formal than a PEP, but like PEPs are intended to record the design
decisions about significant new features or changes.

EEPs are not required for bugfixes or small improvements such as new
TraitsUI editors or Chaco plot types; rather they are reserved for more
substantial changes to design and architecture, or significant new features
where high-level design is important.


What is ETS?
============

ETS is the Enthought Tool Suite, a collection of open source libraries for
the rapid development of desktop scientific software applications. [2]_


ETS Maintainers and EEP Acceptance
==================================

Each ETS project has a maintainer (usually an Enthought employee).  The
maintainer of each project is ultimately responsibe for the acceptance or
rejection of any EEP for their project.  For proposals which cover multiple
projects, if there is disagreement between maintainers, then Mark Dickinson
has the final say.

=============== ===========================
Project         Maintainer
=============== ===========================
Traits          Mark Dickinson
Pyface/TraitsUI Corran Webster
Envisage        Mark Dickinson
Apptools        Robert Kern
Kiva/Enable     John Wiggins
Chaco           Joris Vankerscharver
Mayavi          Prabhu Ramachandran
=============== ===========================

Index
=====

======================== =====================================================
EEP                      EEP Title
======================== =====================================================
`EEP-0 <eep-0.html>`_    EEP Purpose and Guidelines
`EEP-1 <eep-1.html>`_    ETS Code Style
`EEP-2 <eep-2.html>`_    Improved Trait Container Types
`EEP-3 <eep-3.html>`_    Trait Observables
======================== =====================================================


References and Footnotes
========================

.. [1] PEP 1, PEP Purpose and Guidelines
   (http://www.python.org/dev/peps/pep-0001)

.. [2] Enthought Tool Suite
   (http://docs.enthought.com/ets)
