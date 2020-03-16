=====================================
EEP 2: Improved Trait Container Types
=====================================

:Author: Corran Webster
:Status: Active
:Type: Standards Track
:Content-Type: text/x-rst
:Created: 2020-01-02
:Post-History: 2020-01-02


Introduction
============

This is a proposal to replace ``TraitListObject``, ``TraitDictObject``
and ``TraitSetObject`` by simpler stand-alone classes that can
independently fire trait change notifications, while keeping compatibility
with existing behaviour via some specialized listeners that provide
backward compatibility.


Motivation
==========

Traits implements its own specialized subtypes of the standard
Python container types (``list``, ``set`` and ``dict``) that are
able to generate notifications when they change.  However the
implementation ties these instances closely to the trait and object
that they are assigned to: in particular, they store weak references
to the ``HasTraits`` instance and the name of the trait, and then
all changes are fired via the appropriate ``*_items`` trait.

This implementation leads to limitations, the most noticable one
being the inability to listen to nested containers (eg. ``List(List)``
or ``Dict(Str, List)`` being commonly desired cases).  As a result
developers often have to write very thin wrapper classes around the
nested container.  [1]_

Instances of these subclasses have to be aware of modifications that
are made to them, and there is no intrinsic reason why they could not
be independently observed.  The refactoring to make this work is likely
to create clearer and simpler code, by separating the concerns of change
tracking and keeping track of objects and names that need to have
``*_items`` events fired.

By making the container instances first-class listenables, we can then
write infrastructure code that either extends the existing trait listeners
(or perhaps replaces it with something better) that can perform chained
listening down into nested containers.

There are also advantages that may be able to be taken advantage of in
TraitsUI list and table editors, where the lists themselves become the
objects being observed without having to track the underlying ``HasTraits``
instance.


Design
======

New versions of the ``TraitListObject``, ``TraitDictObject`` and
``TraitSetObject`` (possibly with different names, for backwards
compatibility) will be written.  They will have two additional
pieces of state beyond the base list class:

- a ``validator`` which is a callable that expects information about
  the change that the object is about to undergo (eg. adding or removing
  items) and either returns a validated replacement for the added items
  or raises a ``TraitError``.

- a list of ``notifiers`` which are callables that are given information
  about the change that the object has just undergone and can do whatever
  they want with that information.

The classes will override all the appropriate base class methods that
mutate the object in place so that they compute information about the
change and call the ``validator``, apply the change, and then call
each of the ``notifiers``.

For example, a list validator would be given the list object, the index or
slice that the change is applied to, the object or sub-list of objects that
will be removed, and the value or list of values that will replace those
objects, and would be expected to return a validated value or list of values
that will then be used in the actual change.

A list notifier would look a lot like a current list items notifier.  It
would expect the list object, the index or slice that was modified, the
object or sub-list of objects that were removed, and the value or list of
values that were added in their place.

For backwards compatibility, there would be validators and notifiers written
that implement the current behaviours.  So the backwards compatibile
validators would hold references to the inner traits of the container to
validate values and would also check that any length constraints were being
maintained.  The backwards compatible notifier would hold a weak reference
to the ``HasTraits`` object and the trait that is being used, and would pass
the change information through to the ``*_items`` event trait after constructing
the appropriate trait event object.

A factory function or thin subclass that populates appropriately could then
be used in place of the current classes.


Implementation
==============

A proof-of-concept implementation for ``TraitListObject`` is avalaible. [2]_

It is expected that the dictionary and set implementations would be very
similar.

To get a feel for how the code might look like, the ``__setitem__`` method
could be implemented this way::

    def __setitem__(self, index, value):
        """ Set self[index] to value. """
        removed = self._get_removed(index)
        if isinstance(index, slice):
            if len(removed) != len(value) and index.step not in {1, None}:
                # will fail with ValueError
                super().__setitem__(index, value)

            added = self.validate(index, removed, value)
            norm_index = self._normalize_slice(index)
            super().__setitem__(index, added)
        else:
            added = self.validate(index, removed, value)
            norm_index = self._normalize_index(index)
            super().__setitem__(index, added)

        self.notify(norm_index, removed, added)

There are standardized utility methods for determining which values are removed
and for normalizing indices and slices.

For backwards compatibilty, we might define a helper class that holds the state
required (eg. weak references to the ``HasTraits`` object, trait names, trait instances,
etc.) and provide a notifier method something like this::

    def notifier(self, trait_list, index, removed, added):
        if not hasattr(self, "trait") or self.trait is None or self.name_items is None:
            return

        object = self.object()
        if object is None:
            return

        # bug-for-bug conversion of parameters to TraitListEvent
        if isinstance(index, slice):
            if index.step in {1, None}:
                index = min(index.start, index.stop)
            else:
                if added:
                    added = [added]
                removed = [removed]
        else:
            if removed is Undefined:
                removed = []
            else:
                removed = [removed]
            if added is Undefined:
                added = []
            else:
                added = [added]
        event = TraitListEvent(index, removed, added)
        items_event = self.trait.items_event()
        if items_event is None:
            items_event = self.trait.items_event()

        object.trait_items_event(self.name_items, event, items_event)

The backwards compatible ``TraitListObject`` interface could then just be a
factory function like this::

    def TraitListObject(trait, object, name, value, notifiers=[]):
        helper = TraitListObjectHelper(trait, object, name)
        return TraitList(
            value,
            validator=helper.validator,
            notifiers=[helper.notifier] + notifiers
        )

The proof of concept implementation is able to pass almost all of the current
tests.


References and Footnotes
========================

.. [1] Traits Issue #281
   (https://github.com/enthought/traits/issues/281)

.. [2] Traits Pull Request #678
   (https://github.com/enthought/traits/pull/678)
