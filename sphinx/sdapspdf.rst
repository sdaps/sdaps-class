sdapspdf package
================

You can use this package to make PDF forms using the SDAPS packages. SDAPS
itself does not give you a way to submit these though.

To use this feature simply use the sdapspdf package, and then enable the PDF
form generation by setting the `pdf_form` option for checkboxes and freeform
boxes.

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

.. code::

    % In the preamble
    \usepackage{sdapspdf}

    % Set the pdf_form option for all boxes (*)
    \ExplSyntaxOn
    \sdaps_context_append:nn{*} {pdf_form=true}
    \ExplSyntaxOff


