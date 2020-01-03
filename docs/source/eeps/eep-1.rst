==============================
EEP-1: Coding Style Guidelines
==============================

:Author: Corran Webster
:Status: Active
:Type: Informational
:Content-Type: text/x-rst
:Created: 2020-01-02
:Post-History: 2020-01-02


ETS projects largely follow the `PEP7`_ and `PEP8`_ coding style guide and
`NumPy docstring standard`_, with some `exceptions`_ derived from Enthought
standard practice. [1]_ [2]_

.. _exceptions:

Exceptions to CPython's Style Guide
===================================

Docstrings
----------

Function and method docstrings should follow the
`NumPy Docstring Standard`_, falling back to `PEP 257`_ if something is
not specified there.

For ``HasTraits`` subclasses, do not include an ``Attributes`` section in the
class docstring. Our API reference generator can extract the necessary
information.

ETS style for docstrings puts a single space after the opening triple-quotes.
Docstrings may or may not have a final blank line, as our documentation
generator does not care.

.. code-block:: python

    class MyClass(HasTraits):
        """ This is a class with a docstring.

        And no final blank line.
        """

Single-line docstrings may either follow `PEP 257`_ and put the closing
triple-quotes on the same line as the docstring or on the following line.
In addition, for a single-line docstring with the closing quotes on the
same line, an additional space may be left after the final character
to provide balance with the opening space.

This means any of following are acceptable:

.. code-block:: python

    def my_function():
        """ Do something that is simple and easy to describe."""
        print('my_function')


    def my_second_function():
        """ Do something that is simple and easy to describe. """
        print('my_second_function')


    def my_third_function():
        """ Do something else simple and easy to describe.
        """
        print('my_third_function')


Imports
-------

Imports should be broken into separate blocks, separated by a blank line:

* Standard library imports.
* Third-party imports (comtraits, PyOpenGL).
* Enthought imports (traits, enaml, chaco, etc.).
* Local imports.

Import statements should usually happen at the top of the module, not inside
functions. There are some standard exceptions to this rule, however.  Much of
the framework APIs in our codebase make heavy use of factory functions to
configure objects in the frameworks. In many cases, these factory functions
should do their imports locally to avoid loading possibly-heavy modules if the
factory is never needed. For example, Envisage ``Plugin`` definitions should
have almost no imports at the top other than what is necessary to define the
traits on the ``Plugin``.

``__init__.py`` files should be empty and contain no imports.  Public APIs
should be exposed instead via a standard ``api.py`` module in the package.

Import statements that need to be broken up across multiple lines should use
parantheses to mark line continuation, not backslashes.

Yes::

    from traits.api import (Float, HasStrictTraits, Str,
        Tuple)

No::

    from traits.api import Float, HasStrictTraits, Str, \
       Tuple

Implicit relative imports are forbidden; all modules should be written as if
``from __future__ import absolute_import`` is at the top of each module. For
imports within the same package, explicit relative imports are encouraged. For
imports outside of a package, use fully-qualified absolute imports. One should
not use explicit relative imports to go up a level and over to another package.

For example, let us say that we have the following package layout::

    my_project/
        foo/
            __init__.py
            abc.py
            def.py
            tests/
                  __init__.py
                  test_abc.py
        bar/
            __init__.py
            ghi.py

``my_project/foo/abc.py`` needs to import the ``DEF`` class from
``my_project.foo.def`` and the ``GHI`` class from ``my_project.bar.ghi``.
The imports should look like this::

    from my_project.bar.ghi import GHI
    from .def import DEF

Not this::

    from my_project.bar.ghi import GHI
    from my_project.foo.def import DEF

Or this::

    from ..bar.ghi import GHI
    from .def import DEF

Tests can use two levels of relative imports to get to the module under test.
So in ``test_abc.py`` we import the ``my_project.foo.abc`` module like so::

    from .. import abc


Traits
------

Traits should be defined at the top of the class definition, before the
methods are defined. Each trait definition should be preceded by a comment
documenting the attribute.  Comments should use Sphinx's ``#:`` convention
so that automated documentation tools can collect them.

Groups of related traits can be grouped with a comment line heading them;
public traits should be closer to the top:

.. code-block:: python

    class Foo(HasTraits):

        # Foo public interface ----------------------------------------------

        #: The X coordinate.
        x = Property(Float)

        #: The Y coordinate.
        y = Property(Float)

        # Internal state traits ---------------------------------------------

        #: The combined (x, y) position.
        _position = Tuple(Float, Float)

Similarly, methods can be broken up by similar comment headings. Methods that
implement a specific interface or override those on a superclass should usually
be called out under their own heading:

.. code-block:: python

    class SubFoo(Foo):

        # ------------------------------------------------------------
        # Foo interface
        # ------------------------------------------------------------

        def foo(self):
            pass

        def bar(self):
            pass

        # ------------------------------------------------------------
        # SubFoo interface
        # ------------------------------------------------------------

        def sub_foo(self):
            pass

        # ------------------------------------------------------------
        # Traits stuff
        # ------------------------------------------------------------

        def __position_changed(self, new):
            pass

        def _get_x(self):
            pass

         def _get_y(self):
            pass


Envisage
--------

For Envisage service IDs, it is *not* recommended to split long
strings to comply with the PEP8-recommended maximum line length; this
makes it more difficult to search for those strings when refactoring
or debugging.  Instead, keep those strings on one line, and decorate
the line with a ``noqa`` comment to prevent the ``flake8`` utility from
complaining about the excessive line length.

Yes::

    MESSAGING_SERVICE = 'canopy.service.messaging.AsynchronousMessagingService'  # noqa

No::

    MESSAGING_SERVICE = ('canopy.service.messaging.'
                         'AsynchronousMessagingService')


Testing
-------

All new code should be tested. Tests should be written in unittest-style
and should be runnable with ``unittest discover``.  ETS libraries should
provide standard scripts (usually called ``etstool.py``) for installing
dependencies and running tests.


Unused code
-----------

Unused code should not be committed to the master branch: please
remove any commented-out code or unreachable code paths before merging
to master.


Logging
-------

In general, library code should not do any logging configuration: for
example, setting levels on loggers, calling ``logging.basicConfig``,
or creating ``logging.Handler`` or ``logging.Filter`` objects.
Library code should restrict itself to creating loggers via the usual

.. code-block:: python

    import logging
    logger = logging.getLogger(__name__)


and then using the various ``logger`` methods to emit log records
(``logger.warn``, ``logger.exception``, etc.).  Logging configuration
should be left to the application.

There's one notable exception to the above rule: top-level ETS library
packages that use logging *should* add a NullHandler for their logger
in their ``__init__.py``.  This prevents ``No handlers could be found
for ...`` warnings from the logging library for applications that use
the library but don't configure logging.

Tests should also avoid making persistent changes to logging
configuration, though they may need to make temporary configuration
changes (for example, to verify that a particular condition is logged
properly).  Any such configuration changes should be reverted before
the test exits, even if the test fails.

Other exceptions:

- It's fine to configure logging in scripts and examples:  those
  count as mini-applications rather than parts of the library.

- Ditto for ``main`` functions in a Python file that are used to
  demonstrate functionality.


Legacy Code
===========

As of the writing of this EEP, there is a significant portion of the ETS
toolbase which is written to a much older, pre-PEP8 style.  This code will
eventually be migrated to PEP8 style using automated tools like Black_.
Contributors should use their best judgement when modifying existing code
about whether to perform a drive-by cleanup or whether to follow the
existing style.


References and Footnotes
========================

.. [1] PEP 7, Style Guide for C Code
   (http://www.python.org/dev/peps/pep-0007)

.. [2] PEP 8, Style Guide for Python Code
   (http://www.python.org/dev/peps/pep-0008)

.. _PEP7: http://www.python.org/dev/peps/pep-0007/

.. _PEP8: http://www.python.org/dev/peps/pep-0008/

.. _NumPy Docstring Standard: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

.. _PEP 257: https://www.python.org/dev/peps/pep-0257/

.. _Black: https://black.readthedocs.io/en/stable/
