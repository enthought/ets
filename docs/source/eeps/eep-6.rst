===============================
EEP 6: Whither Apptools? [#f1]_
===============================

:Author: Corran Webster
:Status: Active
:Type: Standards Track
:Content-Type: text/x-rst
:Created: 2020-10-01
:Post-History: 2020-10-01


Introduction
============

Apptools is a collection of packages that provides services for ETS
applications.  This EEP is a discussion about how this package can be
refactored to be more useful.


Motivation
==========

Apptools provides a number of sub-packges to help build ETS applications.
Some of these, like ``apptools.preferences`` provide core functionality
for applications, while others are not currently used at all.  We are
planning to migrate Apptools to be Python 3 only, and eventually to make
use of new features from Traits and TraitsUI.  We don't want to do any
migration of code that is not being used.

There is some code in Apptools that provides low-level application
services, such as the code for object persistence, and others, such as the
help subpackage, that are strongly tied to GUI components.  Some, like
``apptools.preferences``, have both aspects: a core application component
and a significant UI component.  And some, like undo, perhaps belong as
a more fundamental part of Pyface or TraitsUI.

Additionally, there are some parts of other ETS packages which may fit
better in an "application support" library: ETSConfig is one, as is the
base Application object and the ResourceManager code from Pyface.  There
has also been discussion that there should perhaps be a place for support
of generic event loops outside of the context of GUIs.

Finally, the interaction of apptools with Envisage is ambiguous: Envisage
depends on some apptools components (such as preferences), but other
components provide Envisage plugins (such as logger and help).


Discussion
==========

This section takes a deeper look at the issues facing Apptools.

Packages Which Are Used and Packages Which are Not
--------------------------------------------------

The following apptools packages are key in either other ETS projects or
heavily used in current Enthought internal projects:

- ``io``
- ``logger``
- ``lru_cache``
- ``persistence``
- ``preferences``
- ``scripting``
- ``selection``
- ``type_registry``
- ``undo``

The following are used in Mayavi, but the use seems to be minor:

- ``naming``
- ``sweet_pickle``
- ``type_manager``

In particular, ``naming`` is optionally imported in the Wx backend to provide
an introspection UI for Python objects; it is not used the Qt, but there is
also no replacement for that functionality.  The ``naming`` sub-package then
depends in turn on features from ``sweet_pickle`` and ``type_manager``.

The following packages duplicate functionality found elsewhere:

- ``appscripting`` has the same goals as ``scripting`` and Canopy's scripting library
- ``io.file`` is essentially a traited version of the Python 3 ``pathlib``
- ``io.h5`` has a lot of overlap with Zarr
- ``permissions`` has some overlap with an internal Enthought closed source library
- ``persistence`` has a versioned pickle which is similar to ``sweet_pickle``
- ``persistence`` has a lot of overlap in its intent with Marshmallow, but using Pickle rather than JSON
- ``template`` is an attempt to generalize templating code used in an internal application
- ``type_manager`` has the same goals as ``traits.adaptation``
- ``type_registry`` code was originally written in QtBinder, and a version still exists there because QtBinder does not want to depend on Apptools.
- ``undo`` provides similar functionality to the TraitsUI history code.

The following packages are used in some Enthought internal legacy applications
that we may want to keep functional:

- ``naming``
- ``sweet_pickle``, which is also used by ``naming`` and ``type_manager``
- ``type_manager``, which is also used by ``naming``

The following packages are not heavily used:

- ``appscripting`` is used by the old ``blockcanvas`` library
- ``help`` is only used in the ``logger`` UI
- ``permissions`` is not used anywhere I could find
- ``template`` is not used anywhere that I could find

Packages Which are Low-level and Which are GUI Packages
-------------------------------------------------------

These packages provide low-level application functionality which may be
of use to CLI or server applications as well as GUI applications, and have
no GUI components:

- ``io``
- ``lru_cache``
- ``persistence``
- ``sweet_pickle``
- ``template``
- ``type_manager``
- ``type_registry``

These packages are purely GUI-oriented:

- ``appscripting``
- ``help``
- ``permissions``
- ``scripting``
- ``selection`` (although it does not have any actual GUI code in it)

These packages have some code which is low-level and some which is GUI
specific.

- ``logger`` provides useful extensions to the core logging module, but also a QA agent UI
- ``naming`` provides a Python implementation of JNDI, but also an explorer UI
- ``preferences`` provides a core library for working with preferences files, but also a library for building preferences screens
- ``undo`` provides command classes that are useful for any command-driven application, but also UI support

Things Which Might Belong in Apptools
-------------------------------------

There are some parts of other libraries which do not fit particularly
well within the general purpose of that library.

The traits ETSConfig library is not heavily used by Traits itself, but
it is core to Pyface, TraitsUI and Enable toolkit discovery.  It also
provides basic application configuration (home directories, company names,
and so forth) that are used by Pyface and Envisage Applications.  It
probably makes sense to move this functionality out of Traits and into a
low-level library alongside some of the parts of apptools.  In doing so it
possibly makes sense to split the toolkit discovery part out from the
application discovery piece.

The base Application object in Pyface is general and does not depend on
any GUI code.  This would comfortably live in a low-level core apptools
library.

The ResourceManager code in Pyface is used for discovery of images, but
is otherwise fairly generic, and might fit well into a low-level apptools
library.

The Workbench system from Pyface, along with its Envisage plugins, would
be better served if it were in a high-level apptools library.  There has
been a general plan to move it for some years now.

The IPython support in Envisage is something of an obstacle to general
development of the plugin framework, so it might comfortably live in a
GUI-level apptools library.

The IPython support has also highlighted a need to be able to support
alternative event loops inside ETS applications, particularly to allow
integration with code that uses ``asyncio`` and similar ``async``-based
Python libraries.  Currently event loop access is provided via Pyface
``GUI`` and some other utility routines, but also having hooks in Traits
to allow UI dispatch.


Things Which Might Not Belong In Apptools
-----------------------------------------

Setting aside parts of apptools that we may not want to support
in the future, there are some pieces of code in apptools that
may work better elsewhere.

The most obvious one is ``undo`` which is fairly fundamental GUI
behaviour, and so probably belongs in Pyface.  It would then be able
to be used for TraitsUI's undo/redo system, replacing the
``traitsui.history`` code, which has shown itself to be buggy.

Similarly, the preferences UI is fairly fundamental, however it uses
TraitsUI, so it may not be a good candidate to move into Pyface.

The ``io.h5`` package has a heavy additional dependency on PyTables.
It may be best in its own package; or with ``PyTables`` carefully
made an optional dependency.

The ``sweet_pickle`` package has no other dependencies outside of
core Python.  It may be best as a stand-alone library.

Things Which Depend on Envisage and Which Envisage Depends On
-------------------------------------------------------------

The main Envisage library depends on ``apptools.preferences``
and ``apptools.io.file``.  The ``single_project`` plugin uses
``sweet_pickle`` and ``naming``.  The preferences dependency
includes both the preferences file reading code, but also the
UI components in the ``envisage.ui`` plugins.

On the reverse side, the ``help`` and ``logger`` packages
provide Envisage plugins.  The ``logger`` plugin also uses
``preferences`` for configuration.  Both of the plugins focus
on contributing UI features, and so are likely fine for inclusion
only with GUI code libraries.

The ``naming`` and ``logger`` packages also hava an optional
dependency on an Envisage ``envisage.project.IWorkspace`` service.
This service does not appear to exist in current ETS code.

These interdependencies can largely be resolved if we were to
have the low-level ``preferences``, ``io.file``, ``naming`` and
``sweet_pickle`` in one library, and the UI-level ``preferences``
and ``logger`` UI code, together with the plugins in a high-level
apptools GUI library.  In particular the UI preferences code is
mostly integrated with Workbench code, so if that were moved to
apptools those dependencies would resolve themselves.

Testing
-------

Much of the code in question was written before Enthought had a
strong testing culture.  The following sub-packages little or no
testing:

- ``appscripting``
- ``help``
- ``logger``
- ``permissions``
- ``template``

This needs to be considered when thinking about refactoring.


Proposal
========

Resolving these issues will likely take some time, and several
releases of Apptools if we are to prevent problems with backward
compatibility.

Step 1
------

Remove the ``appscripting`` and ``template`` modules.

These are not used by any current code, and so there seems little
point in updating them for Python 3.

Step 2
------

Evaluate the ``permissions`` submodule to see if it fits Enthought's
current needs for application permissioning, in particular if it can
integrate well with Enthought's current closed source identity service.

If it is not fit for purpose, it should be removed.  Otherwise it
should have tests written for it.

Step 3
------

Write at least minimal tests for ``help`` and ``logger``; and check
and improve test coverage of other modules which are to be kept.

These are required before any migration to Python 3 only should be
attempted, so we have some indication of the validity of the code after
migration.  At this point there may be a value judgement to be made
about keeping or removing particular modules within the sub-packages
if they are not particularly useful and the effort of testing is more
than their value.

Step 4
------

Migrate the codebase to support only Python 3.6+, Traits 6.0+, and
TraitsUI 7.0+.

Step 5
------

Deprecate ``type_manager`` and convert Apptools code that uses it to
use ``traits.adaptation``.

Everything that it does is covered by ``traits.adaptation``.  We
will keep it around, since it may be used by external code.  Converting
Apptools code such as ``naming`` to ``traits.adaptation`` may possibly
break some external code, but fixes should be straightforward.

Similarly look at ``sweet_pickle`` and, if the decision is to remove it,
then deprecate the sub-package and convert code that uses it.

Step 6a (Optional)
------------------

Copy Undo from Apptools to Pyface.  Deprecate in Apptools after next
Pyface release.

This step can be done at any point from here out, but it would
make some sense to do it before the 5.0.0 release.

Step 6b (Optional)
------------------

Copy Workbench from Pyface and Envisage to Apptools.  Deprecate in
Pyface and Envisage.

This step can be done at any point from here out, but it would
make some sense to do it before the 5.0.0 release.

Step 7
------

Release Apptools 5.0.0.

Ideally this release would include documentation of the packages
which we have long-term interest in keeping.  This provides an
initial release which code that depends on Apptools can use as a
stepping stone as things are further refined.

Step 8
------

Update Apptools to use Traits 6.1+ features.

This should include replacing any TraitHandlers defined in the
library with TraitTypes.

Step 9
------

Split out the core application services into a new package.

This new package can be in the same github repository, at least
initially.  It should, however, be packaged as a different
distribution.  The main Apptools library should import from these
modules in such a way as to not break existing code as much as
possible.  The old import locations should be soft-deprecated.

The only dependencies of code in this package should be on Traits
and

Packages that should be in the new package are:

- ``io``
- ``lru_cache``
- ``persistence``
- ``sweet_pickle`` (only if it is being kept)
- ``type_registry``

plus the non-GUI parts of

- ``logger``
- ``naming``
- ``preferences``

Step 10 (Optional)
------------------

Move other code from ETS packages into this new package.

This might include a base Application object, an ETSConfig
replacement and so on.  These can be added at any point release
from here out, and may be driven more by the release plans of
the packages that they are being moved out of than Apptools.

Step 11
-------

Release the new package.

Step 12
-------

Release Apptools 5.1.0 with the dependencies on the new package.

Step 13
-------

Update Envisage and any other libraries that use Apptools to import
and use the new package where appropriate, and release.

Step 14
-------

Once all ETS dependencies have been fixed to use the new pacakge,
hard-deprecate the old API in Apptools.

Step 15
-------

Before releasing Apptools 6.0.0, remove all deprecated code.

This may be a long way off.

Unknowns
========

We are proposing a new ETS package between Traits and Pyface/Envisage.
It is not clear what it should be called.

Notes
=====

.. [#f1] `Whither Canada? <https://en.wikipedia.org/wiki/List_of_Monty_Python%27s_Flying_Circus_episodes>`_
