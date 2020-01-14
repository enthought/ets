========================
EEP 3: Trait Observables
========================

:Author: Corran Webster
:Status: Active
:Type: Standards Track
:Content-Type: text/x-rst
:Created: 2020-01-02
:Post-History: 2020-01-02


Introduction
============

This is a proposal to add a new, simpler and cleaner, parallel notification
system to the current trait listeners, with the eventual intent of replacing
the existing listeners in new code, and eventually deprecating for old code.


Motivation
==========

Traits is a successful, battle-tested object model system that has been used
extensively inside and outside Enthought for 15 years.  It does what it does
fairly well but, as with any complex system that has grown somewhat
organically, there are issues with it.

Perhaps the biggest problem with the current system is the high cognitive load
in some areas.  Principal amongst these is the listener system, with its
complex system of function signatures and extended trait change descriptions
and the introspection which is required to make this work.  A common cause of
bugs is the failure to anticipate every circumstance that a trait change
handler might be called under, particularly given that changing the signature
can change when an extended trait change handler is called.  Additionally,
there are known bugs in the extended trait change system where behaviour
doesn't match documentation under some circumstances. [1]_ [2]_

An obvious question is why we don't simply fix or replace trait listeners.
The core problem is that even basic "bugfixes" or improvements potentially
break things in hard to diagnose ways. [3]_

By building a similar but cleaner alternative, we allow legacy applications
to continue to run as-is, but provide a straightforward update path.

This proposal in many ways follows the successful change made in the
Traitlets library to introduce an `observe` method and decorator, although
this proposal is to use an object rather than a dictionary to hold information
about the state as that allows code to more easily understand what change took
place and what information is being provided. [4]_


Design
======

Observables are a replacement for trait listeners.  They are to be implemented
alongside the existing listener infrastructure because so much code depends on
the current behaviour.  In many ways they will resemble ``on_trait_change``
but use ``observe`` instead.  The primary differences are:

* observers pass lightweight event objects to their callbacks, rather than the
  (confusingly) different function signatures that listeners currently use.
* the extended trait change syntax will be simplified and behaviours
  standardized
* container objects become more first-class, so if you have a list of lists,
  you can listen to ``foo.items.items`` (or some similar construct)

To use the new observable system, users will use a new ``observe`` method and
corresponding decorator for ``HasTraits`` classes::

    class Example(HasTraits):
        x = Float

        @observe('x')
        def x_updated(self, event):
            print('x updated')

    example = Example()
    example.observe(print, 'x', dispatch='ui')
    example.x = 5.0
    example.observe(print, 'x', remove=True)

The callback or decorated function is expected to accept just one argument, an
event object.  This object will be an instance of new ``TraitEvent`` classes,
which will either be ``namedtuple`` subclasses or classes with ``__slots__``
and a limited collection of attributes. The most basic of these will be for
standard trait changes, and will have attributes for ``object``, ``name``,
``old`` and ``new``, but for example list events would have attributes for
``index``, ``removed`` and ``added``, and extended trait change events should
include additional attributes that give context about which part of the
extended trait change expression was invoked, and the base object being
observed.

Container Objects
-----------------

Presuming EEP 2 [5]_ is approved and implemented, the traits container types
(``TraitListObject``, etc.) will be first-class observables, so users will be
able to write things like, for example::

    class ListExample(HasTraits):

        l = List(Instance(Example))

        @observe('l.items')
        def l_updated(self, event):
            if event.name == 'l':
                print("Whole list changed.")
            elif event.name == 'items':
                print("List modified in-place.")

    list_example = ListExample()
    example.l.observe(print, 'items')

or even::

    l = TraitList()
    l.observe(print, 'items')

Observation Mini-Language
-------------------------

The last piece is to simplify the extended trait change syntax.  We keep the
'.' and ':' as before, but this combined with the ability to listen directly
to containers means we don't need '[]' any more, so we can translate:

- ``l`` remains ``l``
- ``l_items`` becomes ``l:items``
- ``l[]`` becomes ``l.items``
- ``l.x`` becomes ``l.items.x``
- ``l:x`` becomes ``l:items:x``

and in addition gain the ability to add more nuanced observations such as
``l.items:x`` or ``l:items.x``, if desired.  To support this, it may help to
have a corresponding property on trait lists, however that would preculde
the use of "items" to avoid conflict with ``dict.items``,  and we might need
some alternative such as "trait_items" or "elements".

We keep the ability to observe to multiple different trait patterns using
``[...,...]`` to observe based on the existence of metadata using '+', and to
specify recursive patterns using '*'.

We may drop the ability to observe based on the absence of metadata, and
matching prefixes; on the other hand it may be simpler to keep support.

Whatever form the langauge takes, it will be clearly specified with a grammar
so that the implementation of the parser can be replaced with another with
minimal difficulty.  Expressed in a similar style to Python's grammar, it
might look something like this:
::

    group: item (',' item)*
    item: term (connector term)*
    connector: '.' | ':'
    term: (union_group | simple_term) ['*']
    union_group: '[' group ']'
    simple_term: NAME | '+' NAME

To support the new language, we also want a way to programatically generate
pattens as an intermediate form.  This intermediate language has the potential
to be more powerful than the text version (eg. by specifying more powerful
metadata matches):

* ``l.items.x`` -> ``obs('l', obs('items', 'x'))``
* ``l:items:x`` -> ``obs('l', obs('items', 'x', quiet=True), quiet=True)``
* ``i.+foo`` -> ``obs('i', obs('', metadata={'foo': not_none}))``
* ``[x,y].z`` -> ``obs(['x', 'y'], 'z')``
* ``[x,y.z]`` -> ``obs(['x', obs('y', 'z')])``


Implementation
==============

Much if this can be implemented using the existing notification system.  At
the core, ``cTrait`` instances have a list of "notifiers" which are callables
that expect a signature of the form ``object, name, old, new``.  The current
trait listeners system wraps the various listener methods to adapt the various
signatures to this standard notifier signature, and in the case of extended
trait listeners, dynamically manages their connection and disconnection.

The new system proposes to use the same mechanism, wrapping the observe
callbacks to take the notification data plus context they hold as state and
build the event.  At its most basic, this looks something like::

    class SimpleTraitEventNotifyWrapper:

        def __init__(self, observer, owner, target):
            self.owner = weakref.ref(owner)
            self.target = weakref.ref(target)
            if <observer is function-style callable>:
                self.observer = observer
            elif <observer is method-style callable>:
                # store weakref to object + unbound method
                ...

        def __call__(self, object, trait_name, old, new):
            # handle event tracers
            ...
            event = SimpleTraitEvent(
                object,
                trait_name,
                old,
                new,
                self.owner(),
                self.target(),
            )
            try:
                if <function-style>:
                    self.observer(event)
                elif <method-style>:
                    if <object exists>:
                        # bind and call
                        ...
            except Exception as e:
                # handle event tracers
                ...
                handle_exception(object, trait_name, old, new)
            else:
                # handle event tracers
                ...

This is very similar in feel to the current ``TraitChangeNotifyWrapper``, but
constructing an event rather than dispatching based on signature.  A similar
collection of notify wrapper subclasses will be needed for different dispatch
targets and extended trait change situations.

References and Footnotes
========================

.. [1] Traits Issue #537
   (https://github.com/enthought/traits/issues/537)

.. [2] Traits Issue #538
   (https://github.com/enthought/traits/issues/538)

.. [3] Traits Pull Request #621
   (https://github.com/enthought/traits/pull/621)

.. [4] Traitlets Pull Request #61
   (https://github.com/ipython/traitlets/pull/61)

.. [5] EEP 2 (`<eep-2.html>`_)

