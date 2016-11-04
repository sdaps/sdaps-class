sdapsbase package
=================

This base package handles many of the core functionalities to make the SDAPS
class work (together with `sdapsarray`). It implements a number of features
which should however not be relevant for many end users. It should not be
neccessary to dive into the `sdapsbase` implementation unless you want to use
some of the more advanced features or even create completely custom layouts.



The context subsystem
----------------------

SDAPS has a system to handle context for the questions. This context is managed
in the global TeX scope. This means that modifications done for example inside
a `multicols` environment will still be seen in the rest of the document. The
context system itself is also hirarchical, so that it is possible to define
different defaults for sections of the document. The most obvious use case for
this might be prefixing all variables within parts of the document with a
certain string. But one could also imagine changing the size of checkboxes
for parts of the document.

Handling context nesting
^^^^^^^^^^^^^^^^^^^^^^^^

The following commands can be used to handle context nesting. Note that SDAPS
makes a best effort to detect errors where begin/end was not used in a balanced
fashion.

* `\\sdaps_context_begin:n`: Begins a context with the given name
* `\\sdaps_context_end:n`: Ends the context again, ensuring the name is correct
* `\\sdaps_context_begin:`: Begins a context with an empty name
* `\\sdaps_context_end:`: Ends a context started with `\\sdaps_context_begin:`
* `\\sdaps_context_begin_local:` Begins a context which automatically ends together with the current TeX group

Managing context variables
^^^^^^^^^^^^^^^^^^^^^^^^^^

* `\\sdaps_context_put:n`: Delete the given variable from the context
* `\\sdaps_context_put:nn`: Set the given variable to the given value (Variants: `nV`)
* `\\sdaps_context_set:n`: Set context variables from the given `key=val` parameters
* `\\sdaps_context_append:nn`: The first argument being a variable to modify, append the value to the existing value
* `\\sdaps_context_clear:`: Completely clear the context


Defining questions and headings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `\\sdaps_qobject_begin:nnn`: Start a new qobject, giving the following arguments:

  * The name of the context group to start
  * The type of the qobject (to be consumed by the SDAPS main program)
  * The title for the metadata

* `\\sdaps_qobject_end:n`: Finish a qobject again, must pass the correct name for checking nesting
* `\\sdaps_qobject_begin:nn`: Same as the first but without giving a context name
* `\\sdaps_qobject_end:`: End a question which did not have a defined context name

Writing further metadata, these commands must be used from within a QObject begin/end block:

* `\\sdaps_answer:n`: Write metadata for an answer which belongs to the current question (context)
* `\\sdaps_range:nnn`: Write metadata for a range:

  * `lower` or `upper` to define the ends of the range
  * The ID of the checkbox to use (zero based) as the first or last (including)
  * The string for the metadata
    Variants: `nno`, `nnf`, `nnV`

Generic commands are also provided to write to `\\g_sdaps_infofile_iow`:
* `\\sdaps_info_write:n`: Variants: `x`
* `\\sdaps_info_write_x:n`: Variants: `x`

Overrides
---------

Overrides allow setting defaults based on the questionnaire ID or based on the
variable name and value of items. Using this feature it would for example be
possible to fill in names into text fields for printing.

.. note::
    Overrides are independent of the context itself.

Commands which adhere to overrides are currently:

* all `checkboxes`
* all `textboxes`

There is only one command to set the overrides string:
* `\\sdaps_overrides_init:n`

As an example:

.. code::

    % The * applies to all questionnaire IDs. The * inside the group will apply
    % to all items. Other than that it is applied based on the variable name
    % and value.
    \sdaps_overrides_init:n{
        *={
          *={},
          tool_letter_latex={default=true}
        },
        qid1={
          var1={box},
          var2={height=2mm},
          var2&1={width=10mm},
        },
        qid2={
          var1={ellipse},
          var2={ellipse,height=7mm},
          var2&1={ellipse,width=7mm},
        },
    }




The rendering subsystem
-----------------------

Checkbox
^^^^^^^^

=================== ===================================================================
Option              Description
=================== ===================================================================
linewidth           The width of the outline (default: 1bp, modification is not supported by the SDAPS main program!)
width               The width of the checkbox (default 3.5mm)
height              The height of the checkbox (default: 3.5mm)
form                The form, either `box` or `ellipse` (default: `box`, usually set internally)
prefix              The variable prefix from the question to prepend (for internal use)
value               The value of the checkbox (for internal use)
fill                The colour to fill the checkbox with (default: `white`)
draw_check          Whether to draw a checkmark on top of the box (default: `false`)
centered_text       Text to overlay over the checkmark (default: `none`)
text                Text to overlay over the checkmark using a minipage (default: `none`)
text_align          The minipage alignment of the overlay (default: `c`)
text_padding        The minipages padding from the outside border of the box (default: `2bp`)
writepos            Whether to output metadata (default: `false`, but set e.g. by sdapsclassic)
ellipse             Pass as a short form for `form=ellipse`
box                 Pass as a short form for `form=box`
=================== ===================================================================

There is only one user facing command to render a checkbox:

* `\\sdaps_checkbox:nn`
  The following arguments can be given:

  * Variable name
  * Value

The behaviour of the checkbox should be changed through the context. This can be done
globally at the start by simply setting a few flags. As an example the following
modifies the linewidth for all boxes, and the size of checkboxes:

.. sdaps:: Example showing modification of the context for checkbox rendering
    :metadata:

    \noindent
    \ExplSyntaxOn
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { * } { linewidth=2bp }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { checkbox } { fill=red }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_set:n { * = {} }
    \sdaps_checkbox:nn {} {}


    \hspace{1em}
    \sdaps_context_set:n { checkbox={ellipse} }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { * } { linewidth=2bp }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { checkbox } { fill=red }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_set:n { * = {} }
    \sdaps_checkbox:nn {} {}

    \newline

    \sdaps_context_set:n { * = { text = X }, checkbox = { width=5mm, height=5mm} }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { * } { linewidth=2bp }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { checkbox } { fill=red }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_set:n { * = {} }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_set:n { checkbox={draw_check} }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { * } { linewidth=2bp }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { checkbox } { fill=red }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_set:n { * = {} }
    \sdaps_checkbox:nn {} {}

    \ExplSyntaxOff

.. todo:: It appears the text is not centered correctly.

.. warning:: It appears setting "writepos" in the example causes an infinite loop while compiling. Obviously this should not happen, the cause for it is unknown at this point!

