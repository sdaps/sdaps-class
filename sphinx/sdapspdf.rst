sdapspdf package
================

You can use this package to make PDF forms using the SDAPS packages. SDAPS
itself does not give you a way to submit these though.

To use this feature simply use the sdapspdf package. You need to wrap everything
containing PDF form elements inside a :environ:`Form` environment. After this
enable form generation by simply setting the ``pdf_form`` option for checkboxes
and freeform textboxes.

.. note::
    The sdapspdf package imports hyperref internally. So some care might need to
    be taken to import it after hyperref itself.

The following extra options are added to boxes and checkboxes:

=================== =====================
Option              Purpose
=================== =====================
pdf_form            Turn on PDF form generation (default: `false`)
default             Allows enabling a checkbox by default (default: `false`, set to `true` to use)
checkboxsymbol      The symbol to use for the checkmark (integer, see PDF specification, default: 8)
=================== =====================

.. warning::
    The default for pdf_form might still change to be `true`.

.. note::
    The SDAPS base package will likely add further macros to make setting these options more convenient.


.. sdaps:: Using PDF forms
    :preamble:
        \usepackage{sdapspdf}
        % Define aliases for the commands we need to use, context_append
        % expands settings, context_set sets them (for the current scope),
        % possibly removing old settings.
        \ExplSyntaxOn
        \let\mycontextappend\sdaps_context_append:nn
        \let\mycontextset\sdaps_context_set:nn
        \let\mycheckbox\sdaps_checkbox:nn
        \let\mytextboxvhstretch\sdaps_textbox_vhstretch:nnn
        \ExplSyntaxOff

    \begin{Form}
      % The \my* commands are aliases that are defined in the praemble

      % Set the pdf_form option for all boxes (*)
      \mycontextappend{*}{pdf_form=true}

      % Or for checkboxes and textboxes separately
      %\mycontextappend{singlechoice}{pdf_form=true}
      %\mycontextappend{multichoice}{pdf_form=true}
      %\mycontextappend{textbox}{pdf_form=true}

      \noindent A checkbox: \mycheckbox{}{} \newline
      \mycontextappend{multichoice}{default=true}
      A checked checkbox: \mycheckbox{}{} \newline
      \mycontextappend{multichoice}{default=true,checkboxsymbol=5}
      A checked checkbox with different symbol: \mycheckbox{}{}

      Please note that the above rendering is slightly broken as the poppler
      PDF renderer maps the checkboxsymbol incorrectly. Acrobat will show the
      other symbol.

      \noindent A non stretching textbox:
      \mytextboxvhstretch{text}{4cm}{0}
    \end{Form}


