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
 * Cells are rendered as much in-order as possible  (important for metadata generation)

Things that are *not* possible currently:

 * Row or column backgrounds
 * Grid lines
 * Modifying the spacings in between rows or columns

.. warning::
    You should *not* add a trailing ``\\`` to finish the last row. This can confuse
    the class in some situation and may cause a fatal warning.

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

    :kwarg align: An arbitrary string to align multiple :environ:`sdapsarray` environments
        to each other. All environments with the same string will be
        aligned. (default: no alignment)
    :kwarg keepenv: Do not modify the parser to consume ``&`` and ``\\`` for alignment.
        Instead, the user must use :macro:`\\sdaps_array_alignment:` and :macro:`\\sdaps_array_newline:`.
        This is only useful for writing custom environments which use :environ:`sdapsarray` internally.
        Normal users should simply put any nested `array` environment into :macro:`\\\\sdapsnested`
        to prevent issues (see below).

    :kwarg colsep: Spacing added on the left/right of every cell. This defaults to :macro:`\\tabcolsep`.
    :kwarg baselineskip: Override the baselineskip used when calculating the distance between rows.
        Can be used to increase the row distance but keep the line separation inside row headers unmodified.
    :kwarg lineskip: Override the lineskip used when calculating the distance between rows (see ``baselineskip``).
    :kwarg lineskiplimit: Override the lineskiplimit used when calculating the distance between rows (see ``baselineskip``).

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
      row = { \_sdaps_array_row_ltr:NNn },
      end = { \_sdaps_array_end_default: },
    }

    \prop_gput:Nnn \g__sdaps_array_layouter_prop { rotated } {
      begin = { \_sdaps_array_begin_default: },
      row_start = { \_sdaps_array_row_start_default: },
      rowhead = { \_sdaps_array_rowhead_default:Nw },
      colhead = { \_sdaps_array_cell_rotated:Nw },
      cell = { \_sdaps_array_cell_default:Nw },
      row = { \_sdaps_array_row_ltr:NNn },
      end = { \_sdaps_array_end_default: },
    }

If you consider modifying the layouter, then please have a look at the relevant
parts of ``sdapsarray.dtx``. Also, please consider submitting modifications for
upstream inclusion so that other people can benefit from new features.

