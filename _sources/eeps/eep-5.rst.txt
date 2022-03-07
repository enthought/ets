================================
EEP 5: TraitsUI Tables and Trees
================================

:Author: Corran Webster
:Status: Active
:Type: Standards Track
:Content-Type: text/x-rst
:Created: 2020-04-21
:Post-History: 2020-04-21

Introduction
============

This EEP proposes creating a new combined Tree and Table editor for
presenting data with a consistent format.

Motivation
==========

The current situation with TraitsUI table and tree editors is not very
satisfactory.  There are 4 Editors available that perform similar sorts
of functions, but all of them have issues and limitations.

TableEditor
    Perhaps the simplest to use, the TableEditor is limited by using
    underlying table widgets which have to load the entire data set
    into memory.  As a result, it is fine for small tables, but is not
    performant for larger data sets (more than a few hundred rows).

TabularEditor
    While overcoming most of the performance issues of the TableEditor,
    the TabularEditor is far less flexible and the TabularAdaptor class
    which is required for usage is difficult for new users to understand.
    Perhaps most importantly, the TabularEditor does not permit the use
    of different styles of editors in the cells.

ListStrEditor
    This follows the same approach as the TabularEditor, with the same
    pros and cons, although it is much easier to use for basic situations.

TreeEditor
    The TreeEditor has similar performance issues to the TableEditor,
    but also has issues caused by multiple ways of writing the model
    code (TreeNode vs. TreeNodeAdapter vs. ObjectTreeNode).  It can
    do multi-column views, but only on Qt, and the columns beyond the
    first have a different and weaker API.

ArrayViewEditor
    A specialized editor for 2D NumPy arrays, it is essentially a
    TabularEditor with a custom adapter.

DataFrameEditor
    A specialized editor for Pandas DataFrames arrays.  Like the
    ArrayViewEditor it is essentially a TabularEditor with a custom
    adapter.

This situation is far from ideal.  For example:

- it may be unclear to new users which editor to use in which situation
- while documentation is better than it was, usage of advanced features
  can be difficult to get right
- sometimes non-optimal choices must be made because of hard constraints,
  such as using a TabularEditor because of performance concerns, but then
  being limited in the ability to customize editing.
- there are differences in capabilities between the toolkits with some of
  the editors.
- some functionality is harder to access than it ought to be, such as
  checkbox columns, or image columns.

This EEP proposes to write a new Editor around a consistent data model that
can be used easily in most common cases, is performant, and can be the one
clear "use this" choice in most cases.  This should include adapters that
allow using the new Editor on top of different data types easily.

Design
======

Underlying Data Structures
--------------------------

Before laying out a design, it is worth thinking about the way that data
is often presented in scientific applications, and how the current Editors
handle it.  We commonly find that there are the following use-cases that we
might want to handle.

Row-oriented Data
    This is the most common: there is a possibly heirarchical set of data
    that we want to display, where each item has a number of fields.  The
    data items are frequently HasTraits instances, and the fields are some
    subset of the traits.

    This style of data is handled acceptably by the current editors, once
    you understand the way to structure things.

    Examples:

    - a list of HasTraits instances
    - a list of dictionaries with similar keys
    - a tree of HasTraits instances
    - a simple DataFrame, viewed as a collection of rows
    - file-system views
    - object heirarchies
    - results of a SQL query

Column-oriented Data
    This occurs when there are multiple data values that are series of
    (usually homogeneous) items.  These series usually share the same
    length.  There is usually no heirarchy to the data, but it is
    possible that there might be groupings of the items in the case
    where things are not homogeneous.

    This type of data is not handled well by current editors.  It can't
    be used with the TableEditor, and requires a heavily customized
    adapter to work with the TabularEditor or TreeEditor.

    Examples:

    - a HasTraits instance with attributes which are lists or arrays
    - a dictionary with values that are lists or arrays
    - a simple DataFrame, viewed as a collection of columns
    - a Chaco ArrayPlotData

Data Cube
    This is an n-dimensional set of (usually numerical) data indexed by
    various categorical values, possibly with a heirarchy associated
    with the categories.

    This type of data is not handled well by any of the current editors.
    There Enthought has an old, proprietary Qt editor for this sort of
    application.

    Examples

    - a Pandas DataFrame, particularly with complex indices.
    - an XArray or similar extensions of the dataframe
    - a data set in tidy format, which can include lists of HasTraits

Homogeneous 2D Data
    This is data where there is no direct preference of rows over columns.
    In this case, the most natural way of indexing into the data is with
    an (i, j) pair, and the values themselves tend to be all similar (or
    very generic), but not heirarchical.

    This is handled reasonably well by the TabularEditor and the
    ArrayViewEditor for simple data types.  There is no good support for
    spreadsheet-style displays in TraitsUI.

    Examples:

    - 2D NumPy arrays
    - image data
    - spreadsheet-style displays

Mappings
    This is data that has a key-value structure, possibly with some grouping
    or even heirarchy to the keys.  The keys are typically strings, but the
    values are often not homogeneous.

    These can be handled by the current editors, but require significant work
    to adapt the data structures to the required form.  Essentially the
    mapping must be converted to a list of pairs.  In some cases a TraitsUI
    View may be a more appropriate UI.

    Examples:

    - dictionaries of simple key/value pairs
    - a HasTraits object
    - Pandas Series objects

Homogeneous 1D Lists
    In this case, we have a sequence object with homogeneous values.
    This is more-or-less the trivial intersection of row-oriented (with
    just one field per row) with column-oriented (with just one column).

    These are handled reasonably well by the current editors.

    Examples:

    - lists of simple values
    - lists of HasTraits objects with one field of interest
    - 1D NumPy arrays

Ideally we would like to be able to handle all of these cases within TraitsUI,
but not necessarily in the same Editor.  However, we can probably avoid the
DataCube use-case as being sufficiently specialized as to be out of scope
for this EEP.

Widgets
-------

The design is also constrained by the widgets that are available in the
respective toolkits.  Both Qt and WxPython have performant versions of:

- a single-column list editor
- a multi-column table/tree editor
- a grid

In WxPython the first two cases are handled by  the DataViewCtrl class,
while Qt provides the more specialized QListView and QTreeView.  WxPython
also includes a PropertyGrid system which may be useful in some situations,
but Qt has no similar widget so it would need to be built from a QTreeView.
In both toolkits, the grid view is a separate widget.

Qt has the strong advantage that the different widgets all use the same
data model interface under the covers; the WxPython toolkits do not have
that advantage, and so if we want to support different widgets, we will
need to write multiple data adapters.

In most widgets there is a way to override the rendering of cells to permit
the substitution of another control, or an arbitrary rendering of contents
(eg. to insert an image or a plot).  The WxPython DataViewCtrl is limited in
that expects every value in a column to be the same data type, and that on
non-Windows platforms the editors are restricted to those provided by Wx
and cannot be customized beyond that.  The Wx Grid is not limited in this way,
but is not heirarchical so any such structure would need to be implemented
in custom code.

So we can easily support in a cross-platform way:

- possibly heirarchial data where the columns are of a set of standard types
- arbitrarily organized non-heirarchical grids

However, that isn't sufficient to cover all currently existing use cases of
the current set of editors.  As a result the target set of features will
be what the Qt TreeViewEditor can support, most critically the ability to
have custom renderers and editors.  Support for Wx may require either a
customized Grid widget or some way to provide needed functionality on top
of the DataViewCtrl.

Data Model
----------

Both WxPython and Qt have abstract model classes that provide a way to
allow the widgets to access data and styling information, however they
have some differences in how they handle heirarchies.  The WxPython
DataViewCtrl model only allows rows to nest, not columns; the WxPython
Grid model doesn't handle nesting at all, and the Qt model allows nesting
inside arbitrary row and column values.  In practice, however, the Qt views
do not make use of this arbitrary nesting, and only make use of row-based
nesting (using the 0 column as the place where nesting is done).

Practically, then, the data model can be taken to be presenting a possibly
heirarchical set of rows, but non-heirarchical columns.  This data model is
a presenter: the underlying data itself can potentially be quite different
in structure, and we should provide a clear interface to allow Traits
adaptation to be used, as well as traditional subclassing, to map the
underlying data structure to the data model.

This does preclude "pivot table"-style data views where there is
heirarchical organization of both the rows and the columns, but they are
sufficiently specialized to deserve their own treatment, and would need
custom implementations of the row and column headers, including custom
rendering, for both toolkits.  This is beyond the scope of what we want
to support.

In addition to the generic interface for the data model, we should write
a number of standard data models for the common situations described above.

The other important aspect is that the data model must be "virtual" for
performance.  We can't be passing data through to the underlying toolkit,
rather the toolkit myst query for the data.  This should be straightforward
to support.

Sorting, Searching, etc.
~~~~~~~~~~~~~~~~~~~~~~~~

Sorting is potentially problematic for virtual models, so we should not
attempt to sort at the widget level, but rather have sorting state part
of the data model so that it can be handled appropriately by the underlying
data.

Styling, Rendering and Editing
------------------------------

When working with TraitsUI, the data will likely be supplied in some form
via the Editor's value, but auxilliary information about aesthetics, all
the way up to possibly the use of custom rendering and editing, will need
to be supplied via other channels; most likely provided to the Editor, but
potentially in a way that can be modified at run-time.  The data model should
be able to be bound to a named trait, if needed, for ease of modification,
and the model and editor should react appropriately to changes, firing UI
updates when needed.

Implementation
==============

Data Model
----------

Perhaps the most critical part of get right is the data model. It cannot
require large numbers of Python objects when displaying part of a large
data structure, such as a NumPy array: in particular, any Python level
constructs required for the editor should at worst scale by the number of
visible cells (possibly plus some for their parents).  Since we are planning
a row-heirarchial design we need to be particularly careful about *requiring*
a Python object for each leaf in the heirarchy.

This leads to a design where the API for getting a value should look something
like::

    def get_value(self, index):
        ...

where index will usually be a tuple of a row index and column index.
In most cases the column index will be an integer, but the row index
may be more complex

Similarly other methods for returning whether an index has children and
accessing aesthetics and renderers and editors, should just take an index
as argument.  It may make sense to have aesthetics grouped into a lightweight
object to make it easier to provide standard styling.

Index Managers
--------------

Internally, the various toolkit data models use their own internal notions
of an index.  For example, each row in a wx DataViewModel has a corresponding
DataViewItem which holds an integer or None as its ID, while
QAbstractItemModel has a more complex system of ModelIndex objects.  These
internal notions of models need to be mapped to more natural row indices that
match the actual data being displayed.  For example, a completely
non-heirachical structure, like a list or array, the natural notion of an
index is an integer.  For a DataFrame it might be a tuple, for other data
structures it may make sense to have some notion of a tree node.  However
there are a few such mappings that are going to be used over and over again,
and it makes sense to extract these into an independent object, rather than
having multiple data models which differ in how they convert.

For example,  an index manager for a flat data structure that indexes with
integers might look like this in the wxPython case::

    class IntIndexManager(BaseIndexManager):

        def get_item(self, index):
            if index == Root:
                return DataViewItem()
            return DataViewItem(index)

        def get_index(self, item):
            id = item.GetID()
            if id is None:
                return Root
            return int(id)

        def get_parent(self, item):
            return DataViewItem(), int(item)

        def get_child(self, row, item):
            id = item.GetID()
            if id is None:
                return DataViewItem(row)
            raise IndexError("Invalid child.")

These structures may not be completely stateless.  For example, although it
is possible to use a tree ordering to map integers item ids to nodes in a
more complex tree structure, this is likely to be computationally inefficient.
In particular for large trees we would like to avoid traversing the entire
tree to enumerate it, but rather would prefer to do it on the fly.

One solution to this is to assign to each row as it is encountered a unique
and repeatable ID.  For example the wxPython PyDataViewModel uses the Python
id() of an object as the DataViewItem ID.  However this requires the object
to persist at least as long as the item.  As a result, more general data
mappers will have to hold some sort of memento that provides enough context
to build the tree structure.

For example, the following uses two dictionaries to map between DataViewItems
and tuple-based indices::

    class TupleIndexManager(BaseIndexManager):

        _parents = Dict()
        _children = Dict()

        def _item_to_id(self, item):
            id = item.GetID()
            if id is not None:
                id = int(id)
            return id

        def get_item(self, index):
            item = DataViewItem()
            for row in index:
                item = self.get_child(row, item)
            return item

        def get_index(self, item):
            index = Root
            while item.GetID():
                item, row = self.get_parent(item)
                index = (row,) + index
            return index

        def get_parent(self, item):
            id = self._item_to_id(item)
            if id is None:
                # XXX or raise - should never happen
                return DataViewItem()
            parent_id, row = self._parents[id]
            return DataViewItem(parent_id), row

        def get_child(self, row, item):
            parent_id = self._item_to_id(item)
            memento = (parent_id, row)
            if memento not in self._children:
                self._children[memento] = id(memento)
                self._parents[id(memento)] = memento
            return DataViewItem(self._children[memento])

There is a fair amount of boxing and unboxing of DataViewItems, so this could
be made more efficient, and a better system of mementos may mean that fewer
dictionaries are needed, but this gets the idea across.  In particular, it may
make sense to remove the wx specific code and work with IDs, and handle the
boxing and unboxing in the DataViewModel.

Qt QAbstractItemModels and QModelIndices have similar sorts ot issues which can
be solved in similar ways, althought the details are slightly different and
the implementation can be done slightly more efficiently because the user data
is richer than just a number.

Writing IndexManagers is finicky, as if you get things wrong you will end
up with segfaults and crashes at the C++ level.  We should ensure that the
core code supplies IndexManagers that cover all the common cases, so that a
user merely needs to select the one that matches their data best.

While rows index managers are likely to be more complex, it makes sense to
also have an index mapper for columns to map numerical columns into whatever
makes most sense for the underlying data.  Frequently this will be a
stright-through mapping, but once can image other uses.

Data Model API Details
----------------------

The data model needs to provide methods that allow the toolkit object to
reconstruct the structure of the model.  This means that we need the
following methods::

    def has_children(self, row_index):
        ...

    def child_row_count(self, row_index):
        ...

    def column_count(self):
        ...

For data and different representations of that data, at a minimum there need
to be the following:

    def get_value(self, index):
        ...

    def get_text(self, index):
        ...

    def get_checked(self, index):
        ...

    def get_decoration(self, index):
        ...

    def get_text_style(self, index):
        ...

    def get_tooltip(self, index):
        ...

    def get_drag_data(self, index, type):
        # if dragging items out is enabled
        ...

    # etc.

and for editable models, we need:

    def set_value(self, index, value):
        ...

    def set_text(self, index, text):
        ...

    def set_checked(self, index, checked):
        ...

    def accepts_drop(self, index):
        ...

    def handle_drop(self, index):
        ...

While text, checked state and/or decorations are the most commonly used data
types, we expect that the views (particularly editable views) should be able
to provide appropriate editors beyond the default text editor.  We may need
additional hints to be provided by the data model in some cases (eg. for a
spinbox cell editor, what are the minimum and maximum values allowed? for a
combobox what are the allowed values).  In some cases we might be able to
infer these from the trait types of the underlying object, or from the dtype
of an array or dataframe, but these may need to be unified in some way by
this layer.  This may potentially tie in with how to handle drag and drop
data types for external dragging and dropping.

Selections
----------

Selections will be available as a list of raw indexes of the selected values:
the exact value will depend on the selection mode.  The TraitsUI editor may
also expose the selected values, if that makes sense, and so we may want an
API method that exposes those values easily.

We should be able to handle selection modes of at least:

    - single cell
    - single row
    - multiple rows
    - single column
    - multiple column

We may also want to be able to handle multiple cell selection and selecting
a contiguous array of rows and columns.

Selection should be handled at the model level so that selections can be
easily shared across multiple views of the same model.  Thought should be
given to making it straightforward to share the selection via the apptools
selection service.

Sorting
-------

Users will want to sort their data, and it can, potentially be done within
the view, rather than in the underlying data.  Sorting large datasets is
potentially problematic from a performance and data storage point of view.
It also may not particularly make sense for a given data model.

In some cases the best way to implement sorting may be at the level of the
IndexMappers, as they control the mapping between logical table indices and
the underlying data, and so could hold a lookup table (essentially an
argsort).

However in other cases it may be that the best way to sort is to push the
request for sorting down to the underlying data structure (eg. in a view of
a SQL query it makes sense for the sorting to be pushed all the way down to
SQL).

So we need to support the option for sorting, but it is the data model which
has to decide how best to handle this.

View Widgets
------------

We want to provide traits-aware wrappers of the toolkit widgets that we are
using.  For greatest flexibility the right way to implement this is at the
level of Pyface, as the WxPython backend does currently with the Grid API.

This allows us to build incrementally: we can focus on getting the Pyface
API right before wrapping in one or more TraitsUI editors, and the TraitsUI
editors can then potentially be written in a largely toolkit-independent way
(similar to the toolkit-independent TabularAdapter and Table Column classes).

The Widgets should handle view configuration matters, such as showing,
hiding and ordering columns, row and column geometry, whether to display
headers, global features like whether the table is read-only, how many
levels to expand by default, event-reporting, and so on.

The widget will most likely be a thin object, mainly responsible for mapping
toolkit features to a common API of traits and methods, and hooking up the
models in a toolkit-appropriate way.


Editors
-------

We intend to implement one Editor that covers all cases, but it may be that
we want to have multiple Editor factories built on top of it for convenience
(in a similar way to the current `ArrayViewEditor` and `DataFrameEditor`).

There may be a case for having different editors that talk to the same model
in the way that Qt's tree, table and list views do, but it should be done
very cautiously and with clear reasoning, and initially implemented at the
Pyface level.

The editor should be able to be implemented in a toolkit-independent way (or
nearly so) by talking strictly against the Pyface API.  If we find things
outside the Pyface API, there is a strong argument that they should be
folded into that API.

Technologies
------------

This should be a test-bed for the new observer framework from Traits.  It
has sufficient complexity that it should be possible to give a good workout
of the capabilties.  This will give feedback on things like the performance,
user-friendliness, and missing features that are needed.  Time should be
taken to fix any substantial problems.

Code Sketches
-------------

End-user code might look something like this at its simplest::

    class Song(HasStrictTraits):
        name = Str()
        artist = Str()
        album = Str()
        genre = Enum(GENRES)
        duration = Float()
        rating = Range(0, 5)

    class Collection(HasStrictTraits):
        songs = List(Instance(Song))

        view = View(
            Item('songs', editor=DataViewEditor())
        )

This should display a flat table with columns for each editable trait of the
Song class in arbitary order.  This may require some effort in the Editor
class to introspect the object being edited to select an appropriate model and
configure it.  This should ideally include using a combobox editor for genre,
a text editor with float conversion for duration, and an integer spinbox for
rating.

Adding a bit of configurability and a selection.  This is similar to the
current TableEditor behaviour::

    class Collection(HasStrictTraits):
        songs = List(Instance(Song))
        selected_song = Instance(Song)

        view = View(
            VSplit(
                Item(
                    'songs',
                    editor=DataViewEditor(
                        columns=['name', 'artist', 'album', 'rating',]
                        selection_name='selected_song',
                        selection_mode='row',
                    )
                ),
                Item('selected_song', style='custom'),
            ),
        )

An alternative view, showing the songs in columns::

    class Collection(HasStrictTraits):
        songs = List(Instance(Song))
        selected_song = Instance(Song)

        view = View(
            VSplit(
                Item(
                    'songs',
                    editor=DataViewEditor(
                        model=ObjectColumnDataModel,
                        rows=['name', 'artist', 'album', 'rating',]
                        selection_name='selected_song',
                        selection_mode='column',
                    )
                ),
                Item('selected_song', style='custom'),
            ),
        )

For something like a Pandas DataFrame containing the same information::

    class Collection(HasStrictTraits):
        songs = Instance(DataFrame)
        selected_index = Int

        view = View(
            Item(
                'songs',
                editor=DataFrameEditor(
                    columns=['name', 'artist', 'album', 'rating',]
                    index_selection_name='selected_index',
                    selection_mode='row',
                )
            ),
        )

Again, appropriate cell editors should be inferrable from the DataFrame.

For more fundamental objects::

    class Collection(HasStrictTraits):
        songs = List(Dict(Str, Any))

        view = View(
            Item(
                'songs',
                editor=DataFrameEditor(
                    columns=['name', 'artist', 'album', 'rating',]
                )
            ),
        )

Here the rows are from the list, the columns the selected keys from the
dictionaries.  It would be good to be able to determine the cell editors,
but that may be too much to expect.  Which leads to::

    class Collection(HasStrictTraits):
        songs = List(Dict(Str, Any))

        view = View(
            Item(
                'songs',
                editor=DataViewEditor(
                    model=ListDictDataModel,
                    columns=[
                        Column(index='name'),
                        Column(index='artist'),
                        Column(index='album'),
                        Column(index='rating', type='int', min=0, max=5),
                    ],
                )
            ),
        )

