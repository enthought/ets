.. Enthought Tool Suite documentation master file, created by
   sphinx-quickstart on Sat Jul 13 15:32:51 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================
Enthought Tool Suite
====================

The Enthought Tool Suite (ETS) is a collection of open-source components
developed by Enthought, our partners and the scientific Python community,
which we use every day to construct custom scientific applications. It
includes a wide variety of components, including:

- an `extensible application framework <https://docs.enthought.com/envisage>`_
- `application building blocks <https://docs.enthought.com/traitsui>`_
- `2-D <https://docs.enthought.com/chaco>`_ and `3-D <https://docs.enthought.com/mayavi/mayavi>`_ graphics libraries
- scientific and math libraries
- developer tools

The cornerstone on which these tools rest is the `Traits <https://docs.enthought.com/traits>`_
package, which provides the observer pattern in Python; its features include
initialization, validation, delegation, notification, and visualization
of typed attributes.

Community support for ETS is available on the `ets-users group <https://groups.google.com/forum/#!forum/ets-users>`_,
and on `stackoverflow (tag "enthought") <https://stackoverflow.com/search?q=%23enthought>`_ .

Traits: Run-Time Type-Checking and Reactive Programming
=======================================================

Traits provides :py:mod:`~.dataclasses`-like type-checked attributes, the
ability to watch and react to changes in attribute values, together with
(optional) automatic GUI generation.

- Documentation: `<https://docs.enthought.com/traits>`_
- Source: `<https://github.com/enthought/traits>`_

.. image:: images/traitsui.png
   :align: right
   :height: 125px

TraitsUI: Easy GUI-Building
===========================

TraitsUI provides a declarative GUI system built on top of Traits.  Reasonable
default values allow incremental improvement from an automatically generated
GUI through to highly customized behaviour.  TraitsUI uses and can interoperate
with PyQt, PySide or WxPython.

- Documentation: `<https://docs.enthought.com/traitsui>`_
- Source: `<https://github.com/enthought/traitsui>`_

.. image:: images/mayavi.png
   :align: right
   :width: 250px

Mayavi: 3D Visualization Application and Library
================================================

Mayavi provides a 3D visualization application, a library for 3D plotting within
IPython, and a library for embedding 3D visualizations into GUI applications
in TraitsUI, PyQt, PySide and WxPython.

- Documentation: `<https://docs.enthought.com/mayavi/mayavi/>`_
- Source: `<https://github.com/enthought/mayavi>`_

.. image:: images/chaco.png
   :align: right
   :width: 250px

Chaco: Interactive 2D Plotting Library
======================================

Chaco provides an interactive 2D plotting library for GUI applications in TraitsUI,
PyQt, PySide and WxPython.

- Documentation: `<https://docs.enthought.com/chaco>`_
- Source: `<https://github.com/enthought/chaco>`_

Envisage: Plug-In Application Framework
=======================================

Envisage is a plug-in application framework for Python inspired by the plug-in
framework of the `Eclipse <https://www.eclipse.org/>`_ IDE.

- Documentation: `<https://docs.enthought.com/envisage>`_
- Source: `<https://github.com/enthought/envisage>`_

Pyface: Low Level GUI Components
================================

Pyface provides a traits-aware wrapper around basic GUI components, providing
a toolkit-agnostic framework for building application UIs.  Pyface uses and can
interoperate with PyQt, PySide or WxPython.

- Documentation: `<https://docs.enthought.com/pyface>`_
- Source: `<https://github.com/enthought/qt_binder>`_

Qt Binder: Low Level Trait Bindings for Qt
==========================================

QtBinder thinly wraps Qt widgets with Traits.  Binder widgets can be used inside
a Traits UI View using a special Item called Bound. Binder widgets can be bound to
model traits using binding expressions.

- Documentation: `<https://qt-binder.readthedocs.io>`_
- Source: `<https://github.com/enthought/qt_binder>`_

Traits Futures: Background Processing for TraitsUI
==================================================

Traits-futures provides a means to fire off a background calculation from a
TraitsUI application, and later respond to the result(s) of that calculation,
leaving the main UI responsive for user interactions while the background
calculation is in progress.

- Documentation: `<https://docs.enthought.com/traits-futures>`_
- Source: `<https://github.com/enthought/traits-futures>`_

Apptools: GUI Application Components and Systems
================================================

Apptools provides a collection of utilities and systems for building GUI
applications, including logging, undo/redo, application-wide selection,
macro recording.

- Documentation: `<https://docs.enthought.com/apptools>`_
- Source: `<https://github.com/enthought/apptools>`_

Kiva and Enable: 2D Vector Drawing and Interaction
==================================================

Kiva provides a 2D vector drawing abstraction over a variety of backends,
including AGG, Cairo, Quartz, QPainter, PDF and PostScript.  Enable adds
Traits-based interactivity and event-handling on top of Qt or Wx.

- Documentation: `<https://docs.enthought.com/enable>`_
- Source: `<https://github.com/enthought/enable>`_

Codetools: Python Code Analysis and Execution
=============================================

Codetools provides tools for analyzing data flow through Python
code and advanced execution contexts that permit observation of
changes to variables as code is executed.

- Documentation: `<http://docs.enthought.com/codetools>`_
- Source: `<https://github.com/enthought/codetools>`_

SciMath: Scientific Utilities Including Units
=============================================

Scimath provides a collection of scientific computation utilities, including
scalar and numpy array quantities with physical units.

- Documentation: `<https://docs.enthought.com/scimath>`_
- Source: `<https://github.com/enthought/scimath>`_

GraphCanvas: 2D Network Visualization (Under Development)
=========================================================

GraphCanvas provides interactive 2D representations of networks and graphs using
Enable and NetworkX.

- Source: `<https://github.com/enthought/graphcanvas>`_

Other Enthought Open Source
===========================

Enthought also offers a number of other open source packages that aren't part
of the wider Enthought Tool Suite, but which will hopefully be of use to the
wider community.

ibm2ieee
--------

The **ibm2ieee** package provides NumPy universal functions ("ufuncs") for
converting IBM single-precision and double-precision hexadecimal floats to
the IEEE 754-format floats used by Python and NumPy on almost all current
platforms.

- Source: `<https://github.com/enthought/ibm2ieee>`_

pywin32-ctypes
--------------

A reimplementation of pywin32 that is pure python. It uses cffi, if available,
otherwise falling back to using ctypes.  There is no need to have a compiler
available on installation or at runtime.

- Documentation: `<https://pywin32-ctypes.readthedocs.io/en/stable/>`_
- Source: `<https://github.com/enthought/pywin32-ctypes>`_

comtypes
--------

**comtypes** is a lightweight Python COM package, based on the ctypes_
FFI library.

- Documentation: `<https://pythonhosted.org/comtypes>`_
- Source: `<https://github.com/enthought/comtypes>`_
