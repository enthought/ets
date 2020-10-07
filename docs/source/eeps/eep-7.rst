=============================
EEP 7: ETS Code Modernization
=============================

:Author: Corran Webster
:Status: Active
:Type: Standards Track
:Content-Type: text/x-rst
:Created: 2020-10-07
:Post-History: 2020-10-07


Introduction
============

All of the ETS codebase, with the exeption of the Codetools module,
supports Python 3.  With the end-of-life of Python 2 in 2020, we want
to move to a Python 3-only codebase.

Additionally, we would like to make use of some of the new features of
Traits 6.1 and remove things which were deprecated in Traits 6.0 and 6.1.
In doing this we want to minimize the disruption to other codebases.

This also presents a plan for dropping support for old versions of the
GUI toolkits (Qt 4, WxPython < 4.1).

Motivation
==========

ETS is a codebase with roots that go back 15 years.  As a result there
is a lot of old code that either doesn't take advantage of new features,
or which is overly complicated because it needs to take into account the
changes in behaviour of code over the past decade and a half.

Currently the codebase supports Python 2.7 and 3.5+ in most cases, with
the notable exception of Codetools.

Supporting Python 2 requires additional effort from the ETS maintainers
and becomes more and more difficult as Python 3 progresses, preventing
us from using new libraries and features in Python 3.  This has already
been done for Traits 6.0, TraitsUI 7.0, Pyface 7.0 and Envisage (not yet
released), and has seen payoff in terms of code simplicity and quality.

Traits 6.1 presents a new observable framework, trait types and better
container objects which resolve a number of issues with the solutions
in Traits 6.0 and before.  There are some improvements to these scheduled
for Traits 6.2 that we may want to take advantage of as they will make the
transition from old code easier.

We have support in the GUI code for releases of the underlying
toolkits which have not been in use for many years.  Just as supporting
Python 2 causes extra effort, so does supporting these older versions
the toolkit.

Finally, the ETS codebase has a mix of code styles and conventions
used over the years.  Part of this modernization should be to use tools
like ``black`` to make sure that ETS passes Flake8 and matches the
`EEP-1 style guide. <eep-1.html>`_  Consistent code style reduces support
effort and makes a codebase more pleasant to work with.

Proposal
========

This proposal talks about the development of the following ETS libraries:

- Envisage (current version 4.9.2)
- Apptools (current version 4.5.0)
- Enable (current version 4.8.1)
- Chaco (current version 4.8.0)
- Mayavi (current version 4.7.2)
- Scimath (current version 4.2.0)
- Graphcanvas (current version 4.1.0)

We might also use this process for Codetools, but the effort there is
likely to be larger since it is more closely bound to the syntax of Python
by the nature of the library.

We propose to support all Python versions that are not yet end-of-life.
At the time of writing this is Python 3.6 through to Python 3.9.  All
new code should support this range of Python versions, and we should no
longer write any new Python 2 code.

All ETS projects which have not yet dropped Python 2 support will do so
in their next major release, which is release 5.0 for all these libraries.

We propose that the next major release of all ETS projects should work
with Traits 6.0, 6.1 and 6.2.  This means that they will not be able to
take advantage of new features of Traits, but hopefully smooths migration
paths.

The minor release after that, 5.1, should drop support for Traits 6.0 and
6.1 and should as much as possible remove everything that has been
deprecated in Traits 6.0.

We propose that for all ETS projects that have not yet dropped Python 2
support that the next major release should support Qt 4.8, Qt 5.6+, and
WxPython 4.0+ as much as possible.  This will likely require modernization
of any WxPython code that these libraries contain, and possibly some minor
fixes to Qt code, but is not likely to be a major effort.

The releases for Pyface 7.2 and TraitsUI 7.2 should drop support for Qt
versions earlier than 5.6 and WxPython 4.0.  This will likely have little
downstream impact, but libraries might also choose to make this change in
their 5.2 releases if they have Qt or Wx-specific code.

Finally, as part of code clean-up, re-formatting to match modern code
style should be done opportunistically during the modernization process.
In particular, bulk clean-up, like running ``black`` over a codebase should
be done at a point where there are not a lot of open PRs, to reduce the
impact from merge conflicts from re-formatting operations.
