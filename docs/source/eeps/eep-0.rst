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

An EEP is an ETS Enhancement Proposal, similar in purpose and conventions
to a Python Enhancement Proposal [1]_.  At present they are intended to be
less formal than a PEP, but like PEPs are intended to record the design
decisions about significant new features or changes.

EEPs are not required for bugfixes or small improvements such as new
TraitsUI editors or Chaco plot types; these should be handled through the
usual GitHub issue and pull request mechanisms.  Rather EEPs are reserved for
more substantial changes to design and architecture, or significant new
features where high-level design is important.


What is ETS?
============

ETS is the Enthought Tool Suite, a collection of open source libraries for
the rapid development of desktop scientific software applications. [2]_


ETS Maintainers
===============

Each ETS project has a maintainer (usually an Enthought employee).  The
current maintainer of the core ETS projects are listed here:

=============== ===========================
Project         Maintainer
=============== ===========================
Traits          Mark Dickinson
Pyface/TraitsUI Corran Webster
Envisage        Mark Dickinson
Apptools        Robert Kern
Kiva/Enable     John Wiggins
Chaco           Joris Vankerschaver
Mayavi          Prabhu Ramachandran
=============== ===========================


EEP Workflow
============

Anyone can make an Enthought Enhancement Proposal by making a pull request
on the EEPs in the main ETS repo's documentation. [3]_ [4]_

That pull request will be reviewed and feedback given on the structure and
content which should be addressed by the proposer before an ETS maintainer
merges the EEP.  This review should be fairly lenient, with the assumption
that any significant issues will come up in subsequent disucssion.

Discussion of the EEP will take place in an issue on the ETS repo opened for
that purpose.  Enthought developers will make an effort to summarize any
internal discussion about an EEP to that issue.

Once the discussion is done, the appropriate ETS maintainers will decide on
whether to approve or reject the proposal.  A proposer can also choose to
withdraw a proposal.

Once a proposal is accepted, one or more issues will be opened in project
repos to track the implementation.


Index
=====

======================== =====================================================
EEP                      EEP Title
======================== =====================================================
`EEP-0 <eep-0.html>`_    EEP Purpose and Guidelines
`EEP-1 <eep-1.html>`_    ETS Code Style
`EEP-2 <eep-2.html>`_    Improved Trait Container Types
`EEP-3 <eep-3.html>`_    Trait Observables
`EEP-4 <eep-4.html>`_    Type Annotation Integration
`EEP-5 <eep-5.html>`_    TraitsUI Tables and Trees
`EEP-6 <eep-6.html>`_    Whither Apptools?
`EEP-7 <eep-7.html>`_    ETS Code Modernization
======================== =====================================================


References and Footnotes
========================

.. [1] PEP 1, PEP Purpose and Guidelines
   (http://www.python.org/dev/peps/pep-0001)

.. [2] Enthought Tool Suite
   (http://docs.enthought.com/ets)

.. [3] ETS Repo
   (https://github.com/enthought/ets)

.. [4] EEPs Document Directory
   (https://github.com/enthought/ets/tree/master/docs/source/eeps)