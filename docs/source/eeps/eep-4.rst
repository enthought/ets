==================================
EEP 4: Type Annotation Integration
==================================

:Author: Corran Webster
:Status: Active
:Type: Standards Track
:Content-Type: text/x-rst
:Created: 2020-01-29
:Post-History: 2020-01-29


Introduction
============

This is a proposal to allow Traits to be recognized by Python's new static
typing infrastructure, primarily to allow integration with IDEs such as
PyCharm and VS Code that can recognize and make use of the information.


Motivation
==========

There is a growing use of basic static typing and type annotation in Python,
as well as things like dataclasses, that are heading in the direction of
Traits-like capabilities.  Similarly, the fact that Traits provide (amongst
other things) typing information about class attributes, means that there is
at least the possibility of integrating with these new tools.

While there is some appeal to using mypy for static type checking, we already
see most of these benefits by using Traits: when combined with a good test
suite, most type mismatches are caught at testing time, and any that are not
are caught at runtime with a clear error message.  There is one concrete place
where static type checking might help, and that is with ensuring that default
values are of the correct type.

A stronger motivation is from the integration with IDEs and similar coding
environments which are aware of type annotations.  These allow coders to
get more detailed information about the classes and APIs that they are using
interactively, reducing the chance of errors and cognitive load.  While
the ETS developers could build plugins for popular IDEs that understand
Traits and can provide similar information, it is not something which is a
high priority compared with generally improving the codebase and adding new
features, and would probably not be the best use of limited development time.

Given this, there is a temptation to bring in deeper integration with type
annotations.  For example, a class definition like::

    class Example(HasTraits):

        value: int = Trait(5)

is fairly clear in its meaning and close to the equivalent ``dataclass``
usage.  However heading in that direction would be a fairly major change
to Traits, and would not permit existing code to enjoy the benefits of
type annotation.

Additionally, there has been substantial change in the design of standard
library support for type annotations (particularly the :module:`typing`
module) through the supported versions of Python (currently 3.5 to 3.8).
This provides technical obstacles in mapping complex :module:`typing` types
to corresponding Traits types.

Finally, because the :class:`HasMetaTraits` class manipulates the structure
of :class:`HasTraits` subclasses substantially, the structure of the runtime
objects end up being quite different from the declared structures.  It is
quite difficult to directly annotate that (for example) the :class:`Int`
trait type, when used like this::

    class Example(HasTraits):

        value = Int()

means that value holds an integer value, rather than an instance of :class:`Int`,
without effectively declaring that :class:`Int` is a sub-type of :class:`int`,
which can then lead to further issues.

As a result, a more conservative approach is warranted, at least initially.
Rather than starting to annotate directly and completely, it makes more sense
to only partically annotate, and to do so with the use of stub files, so that
the type annotation is distinct from the source code; this also permits some
more freedom in the way that we annotate.


Design
======

Initially, we propose adding stub files for the basic trait types, with the
following restrictions:

- we only attempt to provide valid annotations for _instances_ of trait types,
  not the _classes_.  That is, we will provide a useful annotation for
  ``Int()`` but not for ``Int``.  There is an ulterior motive in this to
  discourage the use of bare classes like ``Int``, as supporting this adds
  some complexity to the codebase.
- for classes with inner traits eg. :class:`List(Int)` we may initially simply
  annotate as :class:`list` rather than using the full :module:`typing` module
  ``List[int]``.  A partial, but true, annotation is better than a complex and
  complete annotation, at least initially.  However initial experimentation
  indicates that it should be possible to cover the inner types.
- following that design, for traits that cannot easily be expressed in terms
  of Python types, we may simply annotate as allowing anything.

This will require some auxilliary type definitions (and likely some generic
types) to describe these situations, but should not require any deep work
with the :module:`typing` module.

Since developing the stub files is an iterative process which is likely to
proceed quickly initially, we do not want to be tied to the Traits release
cycle.  Consequently the stub files should be initially delivered as a
stub-only package ``traits-stubs`` targetting the Traits 6.0 release, with a
plan to merge the stubs into the main traits package once the ETS developers
agree that they are mature and useful.  We do want the stubs to be
included in the long-term, as that gets around deployment problems and
the issue of keeping stubs synchronized with the traits release.

We won't be able to give typing hints for:

- ``**traits`` keyword arguments: if a user wants this they will need to
  express it themselves in the signature of the :method:`__init__` as the
  typing system has no way to link the keyword arguments with particular
  named attributes.  Fortunately these will be run-time type-checked.
- overloaded defaults of the form::

    class Base(HasTraits):
        x = Int()

    class Subclass(Base):
        x = 5

- trait listeners: there is no way to automatically connect traits to
  specially named methods or :func:`on_trait_change` decorators and
  use that to give typing information to the callbacks.
- properties and delegates are similarly likely to be difficult, as
  behaviour may depend on run-time values, or on looking up signatures
  of specially-names methods.


Implementation
==============

A reasonably initial step may be to use stub generation tools to generate
stub files for most of the modules.  However most of the work will need to
be done with the :module:`traits.trait_types` module, since those need to
be converted into something that represents the

For example, a stub file annotation for the :class:`Int` might, in the
simplest possible approach, look like::

    def Int(default_value : int = ..., **metadata) -> int: ...

This is clearly a lie, but is an 80% solution that captures many use-cases.

More likely, we will need to make trait types look like descriptors.
Something like the following works for simple trait types::

    class _TraitType(BaseTraitHandler, Generic[_Accepts, _Stores]):
        default_value: _Stores = ...
        metadata: Dict[str, Any] = ...
        def __init__(self, default_value: _Stores = ..., **metadata: Dict[str, Any]) -> None: ...
        def init(self) -> None: ...
        def get_default_value(self) -> Tuple[int, _Stores]: ...
        def clone(self, default_value: _Stores = ..., **metadata: Any) -> 'TraitType': ...
        def get_value(self, object: Any, name: str, trait: Optional[Any] = ...) -> _Stores: ...
        def set_value(self, object: Any, name: str, value: _Accepts) -> None: ...
        def __call__(self, *args: Any, **kw: Any): ...
        def as_ctrait(self): ...
        @classmethod
        def instantiate_and_get_ctrait(cls): ...
        def __getattr__(self, name: Any): ...

        def __get__(self, object: Any, type: Any) -> _Stores: ...
        def __set__(self, object: Any, value: _Accepts) -> None: ...

We will likely have to make use of definition overloading for traits with
more complex signatures, particularly for constructors.  Some experimentation
will be needed to find the best approach for individual trait types.

For lists and similar trait types with inner traits, it is possible to express
constructs like ``List(Int)`` and ``List(Int())`` with something like::

    class List(_TraitType[_Sequence[_S], _List[_T]]):
        def __init__(
            self,
            trait: Union[_TraitType[_S, _T], _Type[_TraitType[_S, _T]]],
            value: _Sequence[_S] = [],
            minlen: int = ...,
            maxlen: int = ...,
            items: bool = ...,
            **metadata: _Dict[str, _Any]
        ) -> None:
            ...

However some further overloading will be needed to cover the full signature
of the class.

With some work, we can hope to cover perhaps 80-90% of typical usage without
giving warnings in cases where.


What is Not Part of this Proposal
=================================

It is important to note that this is _not_ a proposal to make Traits aware
of type annotations, as in this example::

    class Example(HasTraits):

        value: int = Trait(5, label='Foo:')

        other_value: str = "Hello"

There might be value in doing this, but it is not part of this EEP.

It's also not part of this proposal to modify the current architecture of
Traits to make it more amenable to type inference.  For example, we are
likely to have to make :class:`TraitTypes` _look_ like descriptors to the
typing system, but it is not the intention to actually _make_ them
descriptors.  Again, there might be value in doing this, but it is not
part of this EEP.

