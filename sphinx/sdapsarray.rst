sdapsarray package
==================

This is a base package for "array" like environments. It really is similar to a
tabularx environment to some extend. Its purpose is much more specialized compared
to tabularx. It is less flexible in the types of layouts that can be realized but
a lot more powerful otherwise. The `sdapsarray` environment has the following
features:

* All :environ:`sdapsarray` environments in the document can be aligned to each other
* The environment can span multiple pages
* Headers will be repeated when page splits are encountered
* The rows/columns can be swapped on the fly
* Different ``layouter`` can be plugged in to modify the rendering
* Fragile content can be used without further preparation
* Contained content is executed exactly once (important for metadata generation)

Things that are *not* possible currently:

* Row or column backgrounds
* Grid lines

.. warning::
    The :environ:`sdapsarray` is **not** a ``tabular`` like environment. It behaves
    in similar ways, but there are fundamental differences, causing some issues:

    * You **must not** add a trailing ``\\`` to the last row.

.. sdaps:: Example of a sdapsarray environment

    The following two \texttt{sdapsarray} environments are almost identical. They
    are both aligned to each other because the \texttt{align} option is set to
    the same value. In the second environment the rows and columnes are swapped
    by setting the \texttt{flip} option.

    \begin{sdapsarray}[align=testing]
      row header & colum header & colum header \\
      row header & cell 1 & cell 2 \\
      row header & cell 3 & cell 4
    \end{sdapsarray}

    \hrule

    \begin{sdapsarray}[flip,align=testing]
      row header & colum header & colum header \\
      row header & cell 1 & cell 2 \\
      row header & cell 3 & cell 4
    \end{sdapsarray}

.. sdaps:: Example of a sdapsarray environment split over two columns using multicols
    :preamble: \usepackage{multicol}

    \begin{multicols}{2}
        \begin{sdapsarray}[align=testing,layouter=rotated]
          colum header 0 & colum header 1 & colum header 2 \\
          row header 1 & cell 1 & cell 2 \\
          row header 2 & cell 3 & cell 4 \\
          row header 3 & cell 5 & cell 6 \\
          row header 4 & cell 7 & cell 8 \\
          row header 5 & cell 9 & cell 10 \\
          row header 6 & cell 11 & cell 12
        \end{sdapsarray}
    \end{multicols}


Layout and formatting considerations
------------------------------------

The following hold true inside the environment:

* The row headers are set into a :macro:`\\vtop` with the left over width from
  the cells. This vertical box is later re-set into a :macro:`\\vbox`. The
  effect is that the interrow skip is calculated between the last element of
  the previous row and the first element of the next row. this means you must
  be careful to not insert invisible content at the start of the vertical box.
  (e.g. by adding a :macro:`\\leavevmode`).
* The exception to the above rule is the start of the environment (i.e. the
  header row) for which the top baseline information is (currently) discarded!
* Each cell is set into an :macro:`\\hbox` with the last skip in the box removed
  again (i.e. trailing space). You can use :macro:`\\hfill` to align the box to
  the left/right but need to prevent the :macro:`\\hfill` to be removed again
  for left alignment (e.g. by adding a ``\kern 0pt``).
* Column headers behave like cells but a special layouter can be assigned to
  them.
* Row headers and column headers will usually be set on a common baseline. The
  exception to this is if the column header contains multiple boxes/lines. In
  that case the cells will be centered ignoring the baselines of both cells
  and row header.
* A penalty of 10 is inserted between rows.


sdapsarray environment
----------------------

.. environ::
    \begin{sdapsarray}[kwargs]
      content with cells delimitted with & and \\
    \end{sdapsarray}

    :kwarg flip: Transpose array making rows to columns (default: ``false``)
    :kwarg layouter: The layouter to use. New layouters can be defined, the following
        exists by default:

        * ``default``: Simple layout centering cells and giving all leftover space to the row
          header which will line break automatically (this is the default)
        * ``rotated``: Similar to default but rotates the column headers

    :kwarg angle: The angle of the header when in ``rotated`` mode
    :kwarg align: An arbitrary string to align multiple :environ:`sdapsarray` environments
        to each other. All environments with the same string will be
        aligned. (default: no alignment)
    :kwarg keepenv: Do not modify the parser to consume ``&`` and ``\\`` for alignment.
        Instead, the user must use :macro:`\\sdaps_array_alignment:` and :macro:`\\sdaps_array_newline:`.
        This is only useful for writing custom environments which use :environ:`sdapsarray` internally.
        Normal users should simply put any nested `array` environment into :macro:`\\sdapsnested`
        to prevent issues (see below).
    :kwarg no_header: Disable column header handling and repeating. Note that this
        setting is independent of whether the ``flip`` option is set. As such, one may
        need to take its value into account when setting it. (default: ``false``)
    :kwarg colsep: Spacing added on the left/right of every cell. This defaults to `6pt`.
    :kwarg rowsep: Extra spacing added between rows. This defaults to `0pt`.

    The ``keepenv`` option should usually not be used by an end user writing a document, it is very useful
    when writing environments which use :environ:`sdapsarray` internally (like :environ:`choicearray`).

    .. macro:: \sdapsnested{content}

        Reverts the ``&`` and ``\\`` to their original meaning. Content in an
        :environ:`sdapsarray` environment can be wrapped with this if it requires
        these characters to be active (i.e. you can use the ``array`` environment
        this way for example).

    .. macro:: \sdaps_array_alignment:

        Alternative to using the ``&`` delimiter between cells. This is useful together
        with the ``keepenv`` kwarg argument. In particular when creating custom environments
        which use sdapsarray internally.

    .. macro:: \sdaps_array_newline:

        Alternative to using the ``\\`` delimiter between cells. This is useful together
        with the ``keepenv`` kwarg argument. In particular when creating custom environments
        which use sdapsarray internally.

    .. sdaps:: Two sdapsarray environments each with a nested array, in one case using the keepenv option.
        :preamble:
            \usepackage{multicol}
            % Wrap the commands with _ as we cannot use them directly. This needs to
            % be a \def and not a \let because they are redefined dynamically internally.
            \ExplSyntaxOn
            \def\sdapsalignment{\sdaps_array_alignment:}
            \def\sdapsnewline{\sdaps_array_newline:}
            \ExplSyntaxOff

        \begin{multicols}{2}
            \begin{sdapsarray}
               & col 1 & col 2 \\
              row header 1 & \sdapsnested{$ \begin{array}{cc} a & b \\ c & d \end{array}$} & cell 2 \\
              \verb^row_header^ & cell 3 & cell 4
            \end{sdapsarray}

            \begin{sdapsarray}[keepenv]
               \sdapsalignment col 1 \sdapsalignment col 2 \sdapsnewline
              row header 1 \sdapsalignment $ \begin{array}{cc} a & b \\ c & d \end{array}$ \sdapsalignment cell 2 \sdapsnewline
              \verb^row_header^ \sdapsalignment cell 3 \sdapsalignment cell 4
            \end{sdapsarray}
        \end{multicols}


Defining a custom layouter
--------------------------

.. warning:: This is an advanced feature and its use a good or even in depth knowledge of how TeX processes boxes and input!

It is possible to register further ``layouter``
which can subsequently used throughout the document. These layouters need to
adhere to a number of rules which will not be explained in detail here.

The following code is a copy of the two predefined layouter not showing the
implementation of the different macros. Visible here is that they only differ
in the method to render the column header ``colhead``, all other methods are
identical.

.. code::

    \prop_gput:Nnn \g__sdaps_array_layouter_prop { default } {
      begin = { \_sdaps_array_begin_default: },
      row_start = { \_sdaps_array_row_start_default: },
      rowhead = { \_sdaps_array_rowhead_default:Nw },
      colhead = { \_sdaps_array_cell_default:Nw },
      cell = { \_sdaps_array_cell_default:Nw },
      row = { \_sdaps_array_row_ltr:NNNN },
      end = { \_sdaps_array_end_default: },
    }

    \prop_gput:Nnn \g__sdaps_array_layouter_prop { rotated } {
      begin = { \_sdaps_array_begin_default: },
      row_start = { \_sdaps_array_row_start_default: },
      rowhead = { \_sdaps_array_rowhead_default:Nw },
      colhead = { \_sdaps_array_cell_rotated:Nw },
      cell = { \_sdaps_array_cell_default:Nw },
      row = { \_sdaps_array_row_ltr:NNNN },
      end = { \_sdaps_array_end_default: },
    }

If you consider modifying the layouter, then please have a look at the relevant
parts of ``sdapsarray.dtx``. Also, please consider submitting modifications for
upstream inclusion so that other people can benefit from new features.

