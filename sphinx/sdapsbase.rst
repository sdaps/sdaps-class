.. _sdapsbase:

sdapsbase package
=================

This base package handles many of the core functionalities to make the SDAPS
class work (together with :environ:`sdapsarray`). It implements a number of features
which should however not be relevant for many end users. It should not be
neccessary to dive into the :ref:`sdapsbase <sdapsbase>` implementation unless you want to use
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

.. macro:: \sdaps_context_begin:n { context name }

    Begins a context with the given name

.. macro:: \sdaps_context_end:n { context name }

    Ends the context again, ensuring the name is correct

.. macro:: \sdaps_context_begin:

    Begins a context with an empty name

.. macro:: \sdaps_context_end:

    Ends a context started with :macro:`\\sdaps_context_begin:`

.. macro:: \sdaps_context_begin_local:

    Begins a context which automatically ends together with the current TeX group.

.. macro:: \sdaps_context_enable_writing:

    Enable metadata writing for the remainder of the current context. Note that
    this package disables writing at start and you need to enable it before
    calling :macro:`\\sdaps_begin:` (and :macro:`\\sdaps_end:`). Classes such as
    the :ref:`sdapsclassic` will enable metadata writing for you.

.. macro:: \sdaps_context_disable_writing:

    Disable metadata writing for the remainder of the current context. Note that
    disabling metadata writing may have some side effects with regard to
    variables and automatic numbering of questions and answers. The exact
    behaviour is currently *not* well defined.

.. macro:: \sdaps_context_hook_end:n

    Register a token list which will be executed at the end of the current
    context. This is primarily useful as a context might be ended implicitly
    in some circumstances.

.. macro:: \sdaps_context_hook_post_end:n

    Register a token list which will be executed *after* the end of the current
    context has ended (i.e. in the parent context). This is primarily useful
    as a context might be ended implicitly in some circumstances.

Managing context variables
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. macro:: \sdaps_context_put:n { key }

    Set the given variable (or key) to ``\\undefined``.

.. macro:: \sdaps_context_put:nn { key } { value }

    Set the given variable to the given value (Variants: ``nV``)

.. macro:: \sdaps_context_remove:n { key }

    Remove the given variable from the context.

.. macro:: \sdaps_context_set:n { key=value, key={a=b, c=d} }

    Set context variables from the given ``key=value`` parameters

.. macro:: \sdaps_context_append:nn { key } { value }

    The first argument being a variable to modify, append the given value to the
    existing value. This can for example be used to change only one aspect of
    checkbox drawing (e.g. ``form``) without affecting resetting another one
    that was defined earlier (e.g. ``width`` or ``height``).

    Generally it is a good idea to use this macro as nested options are common.

    Identical to :macro:`\\sdaps_context_append:nnn` with "``,``" as the separator.

.. macro:: \sdaps_context_append:nnn { key } { value } { separator }

    Append the value to the given ``key`` in the context. If ``key`` is set,
    inserts ``separator`` between them. If key is not set, simply sets the
    ``key`` to the given value.

    :Variants: ``nVn``


Defining questions and headings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. macro:: \sdaps_qobject_begin:nnn { name } { type } { title }

    Start a new qobject, giving the following arguments:

    * The name of the context group to start
    * The type of the qobject (to be consumed by the SDAPS main program)
    * The title for the metadata

.. macro:: \sdaps_qobject_end:n { name }

    Finish a qobject again, must pass the correct name to verify correct nesting.

.. macro:: \sdaps_qobject_begin:nn { type } { title }

    Same as :macro:`\sdaps_qobject_begin:nnn`  but without giving a context name.

.. macro:: \sdaps_qobject_begin_local:nn { type } { title }

    Same as :macro:`\sdaps_qobject_begin:nnn`  but will automatically end with
    the current TeX group (using :macro:`\sdaps_context_begin_local:`).

.. macro:: \sdaps_qobject_end:

    End a question which did not have a defined context name

You can write further metadata using the following macros:

.. macro:: \sdaps_qobject_append_var:n { var }

    Appends the given string to the variable name of the question. An ``_``
    will be used to separate the new variable name with any piece that was
    defined earlier (either on the same question or on a surrounding question
    object).

    If ``var`` starts with an underscore (``_``) then an implicit variable name
    for all surrounding question object (i.e. headings/sections) will be
    generated based on their automatic numbering. This is similar to the
    mechanism used by :environ:`choicearray` to ensure that the different questions
    can always be told appart, even if the user did not specify a variable name
    for all of them.

.. macro:: \sdaps_answer:n { answer text }

    Write metadata for an answer which belongs to the current question (context)

.. macro:: \sdaps_range:nnn { lower|upper } { ID } { answer text }

    Writes metadata for a range.

    :arg lower|upper: Give either ``lower`` or ``upper`` for each end of the range.
    :arg ID: The ID of the checkbox which corresponds to the first/lower or
        last/upper box in the range. Other boxes are considered outside and need a
        separate answer. Boxes are counted zero based and the given range is inclusive.
    :arg answer text: The string for the metadata.

    :Variants: ``nno``, ``nnf``, ``nnV``

Generic commands are also provided to write to

.. macro:: \sdaps_info_write:n { text }

    Write given text to metadatafile at shipout. Some output may be reordered due
    to this, but all SDAPS classes ensure that the metadata can still be decoded
    correctly. As this macro leaves elements in the output stream it can affect
    layouting in a few cases (e.g. row headers of :environ:`sdapsarray`).

    The tokens **will not be expanded** again before writing. This implies that coordinates
    cannot be written using this macro.

    :arg text: Text to write to the metadata file.

    :Variants: ``x``

.. macro:: \sdaps_info_write_x:n

    Write given text to metadatafile at shipout. Some output may be reordered due
    to this, but all SDAPS classes ensure that the metadata can still be decoded
    correctly. As this macro leaves elements in the output stream it can affect
    layouting in a few cases (e.g. row headers of :environ:`sdapsarray`).

    The tokens **will be expanded** again before writing. This implies that coordinates
    can be written using this macro if one takes care not to protect them from
    being expanded at macro execution time.

    :arg text: Text to write to the metadata file.

    :Variants: ``x``

Overrides
---------

Overrides allow setting defaults based on the questionnaire ID or based on the
variable name and value of items. Using this feature it would for example be
possible to fill in names into text fields for printing.

.. note::
    Overrides are independent of the context itself.

Commands which adhere to overrides are currently:

* all ``multichoice`` or ``singlechoice`` checkboxes
* all ``textboxes``

There is only one command to set the overrides string:

.. macro:: \sdaps_set_questionnaire_id:n { ID }

    Set the current questionnaire ID. This should generally not change unless
    some sort of concatenation is done. It is only relevant for writing new
    environments.

.. macro:: \sdaps_overrides_init:n { overrides }

    :arg overrides: A key=value argument with all the override definitions. 

    Each of the override definitions will be appened to the items keys if it is
    matching. Matching happens first based on the questionnaire ID with ``*``
    being allowed as a wildcard, and then based on variable name and value. The
    second level (name and value) is either just the variable name or the variable
    name and value separated by an ``&`` character.

    This gives six matches with increasing priority:

    * wildcard questionnaire ID, wildcard target
    * wildcard questionnaire ID, matching variable
    * wildcard questionnaire ID, matching variable, matching value
    * matching questionnaire ID, wildcard target
    * matching questionnaire ID, matching variable
    * matching questionnaire ID, matching variable, matching value

    .. sdaps:: Overriding checkbox color and pre-filled value based on
        questionnaire ID and variables.
        :sdapsclassic:
        :metadata:
        :preamble:
            \ExplSyntaxOn
            \sdaps_overrides_init:n{
                % For all questoinnaires independent of their ID
                *={
                  % For all elements which use the overrides
                  *={fill=green},
                  % Specific element with that variable name
                  flower_bob_alice={draw_check=true},
                  % Specific element with variable "var" and value 1
                  var&1={draw_check=true},
                },
                % Specific questionnaire ID
                testid={
                  % We need to explicitly unset it again!
                  flower_bob_alice={draw_check=false},
                  flower_adam_alice={draw_check=true},
                },
            }
            \ExplSyntaxOff

        \begin{choicegroup}[var=flower]{A group of questions with variable "flower"}
          \groupaddchoice[var=alice]{Choice "alice"}
          \groupaddchoice[var=eve]{Choice "eve"}
          \choiceline[var=adam]{Question "adam"}
          \choiceline[var=bob]{Question "bob"}
        \end{choicegroup}

        % Force a different questionnaire ID (never do this in a real document!)
        \ExplSyntaxOn
        \sdaps_set_questionnaire_id:n { testid }
        \ExplSyntaxOff
        \begin{choicegroup}[var=flower]{A group of questions with variable "flower"}
          \groupaddchoice[var=alice]{Choice "alice"}
          \groupaddchoice[var=eve]{Choice "eve"}
          \choiceline[var=adam]{Question "adam"}
          \choiceline[var=bob]{Question "bob"}
        \end{choicegroup}


The rendering subsystem
-----------------------

Checkbox
^^^^^^^^

=================== ===================================================================
Option              Description
=================== ===================================================================
linewidth           The width of the outline (default: 1bp)
width               The width of the checkbox (default 3.5mm)
height              The height of the checkbox (default: 3.5mm)
form                The form, either `box` or `ellipse` (default: `box` for `multichoice` and `ellipse` for `singlechoice`)
value               The value of the checkbox (for internal use)
fill                The colour to fill the checkbox with (default: `white`)
draw                The colour to draw the checkbox frame with (default: `.`, i.e. current text colour)
draw_check          Whether to draw a checkmark on top of the box (default: `false`)
centered_text       Text to overlay over the checkmark (default: `none`)
text                Text to overlay over the checkmark using a minipage (default: `none`)
text_align          The minipage alignment of the overlay (default: `c`, valid are **c**enter, **t**op, **b**ottom or **s**pread)
text_padding        The minipages padding from the outside border of the box (default: `2bp`)
ellipse             Pass as a short form for `form=ellipse`
box                 Pass as a short form for `form=box`
=================== ===================================================================

There is only one user facing command to render a checkbox:

* `\\sdaps_checkbox:nn`
  The following arguments can be given:

  * Variable name
  * Value

The behaviour of the checkbox should be changed through the context. On a first
level this works by using `\\sdaps_checkbox_set_type:n` and setting either
`singlechoice` or `multichoice`. Other than that you can also change the style
for `singlechoice` and `multichoice` through the context and overrides. The
following example demonstrates the use of context modification.

.. sdaps:: Example showing modification of the context for checkbox rendering

    \noindent
    \ExplSyntaxOn
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { * } { linewidth=2bp }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { multichoice } { fill=red }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_set:n { * = {} }
    \sdaps_checkbox:nn {} {}


    \hspace{1em}
    \sdaps_context_set:n { multichoice={ellipse} }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { * } { linewidth=2bp }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { multichoice } { fill=red }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_set:n { * = {} }
    \sdaps_checkbox:nn {} {}

    \newline

    \sdaps_context_set:n { * = { centered_text = X }, multichoice = { width=5mm, height=5mm} }
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
    \sdaps_context_set:n { multichoice={draw_check} }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { * } { linewidth=2bp }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_append:nn { multichoice } { fill=red }
    \sdaps_checkbox:nn {} {}

    \hspace{1em}
    \sdaps_context_set:n { * = {} }
    \sdaps_checkbox:nn {} {}

    \ExplSyntaxOff

.. todo:: It appears the text is not centered correctly.

