Creating custom layouts using base commands
===========================================

Usually the pre-defined layouts that SDAPS provides are sufficent. However,
there may be special cases that need more customization. Such customization is
possible, but it does require a more in depth understanding of LaTeX and
the SDAPS packages.

If you do this, please make sure to properly test the output. The easiest way
of such testing is to use the ``annotate`` command that SDAPS provides, as it
visualises the view that SDAPS has of the questionnaire. Doing this testing is
essential as small errors and even side effects of how LaTeX executes code may
render the information about the questionnaire useless!

Even seemingly "simple" environments like ``tabularx`` may not be usable
together with SDAPS!


General question structure
--------------------------

To define a question, you need to define
1. the start of the question and its type,
2. the possible answers to the question
3. the checkboxes and textboxes, and finally
4. the end of the question.

A very simple example might look like the following.

.. sdaps:: Question with one checkbox
    :sdapsclassic:
    :metadata:

    % Prepare some stuff so that we can access the specialized commands more easily.
    \ExplSyntaxOn
    \let\myquestionbegin\sdaps_qobject_begin:nnn
    \let\mycheckbox\sdaps_checkbox:nn
    \let\myanswer\sdaps_answer:n
    \let\myquestionend\sdaps_qobject_end:n
    \ExplSyntaxOff

    \myquestionbegin{name}{Choice}{Exported question text}
    Please check after reading this text: \mycheckbox{}{}
    \myanswer{check}
    \myquestionend{name}

Please have a look at the resulting document and the generated metadata. In particular,
please note:

* The export shows "``QObject-Choice``" this is from the ``Choice`` specified and denotes the question type
* The ``name`` argument does not show up. It only needs to match the one at the end and primarily serves error detection purposes.
* SDAPS will see the question as "Exported question text" with one answer "check"
* The checkbox is automatically exported including its coordinates

.. warning::
    Be careful! The below example shows the effect that ``tabularx`` has. This environment
    expands its content multiple times, and the result is that the automatic numbering
    breaks; making this the 3rd question rather than the first! Other subtle errors like
    this can occur with certain environments, so make sure to double check everything is OK!

    .. sdaps:: Question inside tabularx
        :preamble: \usepackage{tabularx}
        :sdapsclassic:
        :metadata:

        % Prepare some stuff so that we can access the specialized commands more easily.
        \ExplSyntaxOn
        \let\myquestionbegin\sdaps_qobject_begin:nnn
        \let\mycheckbox\sdaps_checkbox:nn
        \let\myanswer\sdaps_answer:n
        \let\myquestionend\sdaps_qobject_end:n
        \ExplSyntaxOff

        \begin{tabularx}{\textwidth}{|X|}
          \myquestionbegin{name}{Choice}{The tabularx environment breaks everything ...}
          Please check after reading this text: \mycheckbox{}{}
          \myanswer{check}
          \myquestionend{name}
        \end{tabularx}


The different question types
============================

Headings
--------

This is the easiest case, and it can be used for structuring the document.

For example, the ``\section`` command simply calls
``\sdaps_qobject_begin:nnn { section }{ Head }{ #1 }``
and ``\sdaps_qobject_end:n { section }`` for you. Something similar happens for
the ``choicegroup`` and other grouping environments where a heading is defined
for all questions.

.. sdaps:: Grouping questions
    :sdapsclassic:
    :metadata:

    % Prepare some stuff so that we can access the specialized commands more easily.
    \ExplSyntaxOn
    \let\myquestionbegin\sdaps_qobject_begin:nnn
    \let\myquestionend\sdaps_qobject_end:n
    \ExplSyntaxOff

    \myquestionbegin{heading}{Head}{Heading}
      Something inside the section.
    \myquestionend{heading}


Multiple choice
---------------

The simple multiple choice question is of type ``Choice``. We already saw the
first example earlier. Simply add more checkboxes and answers as needed. SDAPS
will match each checkbox to one answer in the order that it finds the defintions.

.. sdaps:: Multiple choice question using itemize
    :sdapsclassic:
    :metadata:

    % Prepare some stuff so that we can access the specialized commands more easily.
    \ExplSyntaxOn
    \let\myquestionbegin\sdaps_qobject_begin:nnn
    \let\mycheckbox\sdaps_checkbox:nn
    \let\myanswer\sdaps_answer:n
    \let\myquestionend\sdaps_qobject_end:n
    \ExplSyntaxOff

    \myquestionbegin{name}{Choice}{Attended events}
    Which of the following events did you attend?
    \begin{itemize}
      \item[\mycheckbox{}{}] \myanswer{Keynote} The Keynote
      \item[\mycheckbox{}{}] \myanswer{Workshop} A workshop
      \item[\mycheckbox{}{}] \myanswer{Party} Our glorious party
      \item Something else entirely \myanswer{other}
        \ExplSyntaxOn
          \sdaps_textbox_hstretch:nnnnn{}{2mm}{5mm}{40mm}{1}
        \ExplSyntaxOff
    \end{itemize}
    \myquestionend{name}

Note that we placed a textbox rather than a checkbox as one of the possible
answers.


Single choice
-------------

We can also define a single choice question. For this, we need to make two
small adjustments. The first is to use the ``Option`` question type. The second
is to tell SDAPS that we would like to use the ``singlechoice`` style for
checkboxes.

The checkbox style change will be in effect for the scope of the question.

.. sdaps:: Single choice question using itemize
    :sdapsclassic:
    :metadata:

    % Prepare some stuff so that we can access the specialized commands more easily.
    \ExplSyntaxOn
    \let\myquestionbegin\sdaps_qobject_begin:nnn
    \let\mycheckbox\sdaps_checkbox:nn
    \let\myanswer\sdaps_answer:n
    \let\myquestionend\sdaps_qobject_end:n
    \let\mysetcheckboxtype\sdaps_checkbox_set_type:n
    \ExplSyntaxOff

    \myquestionbegin{name}{Option}{Attended events}
    \mysetcheckboxtype{singlechoice}
    Which one of the following events did you attend?
    \begin{itemize}
      \item[\mycheckbox{}{}] \myanswer{Talk room A} Talk in room A
      \item[\mycheckbox{}{}] \myanswer{Talk room B} Talk in room B
      \item Something else entirely \myanswer{other}
        \ExplSyntaxOn
          \sdaps_textbox_hstretch:nnnnn{}{2mm}{5mm}{40mm}{1}
        \ExplSyntaxOff
    \end{itemize}
    \myquestionend{name}

Note that we placed a textbox rather than a checkbox as one of the possible
answers.


Ranges
------

Quite often one has single choice question which represent a value on a range.
One could create these using the ``Option`` type question, but with ``Range``
it becomes more convenient.

Range questions can contain a single range and further answers like
"Not applicable".

The range is specified with a separate command. For the purpose of this command,
the first and last box that is part of the range needs to be specified. This is
done with a zero based index (i.e. the first checkbox is 0, the second 1, …).

.. sdaps:: Range question
    :sdapsclassic:
    :metadata:

    % Prepare some stuff so that we can access the specialized commands more easily.
    \ExplSyntaxOn
    \let\myquestionbegin\sdaps_qobject_begin:nnn
    \let\mycheckbox\sdaps_checkbox:nn
    \let\myanswer\sdaps_answer:n
    \let\myrange\sdaps_range:nnn
    \let\myquestionend\sdaps_qobject_end:n
    \let\mysetcheckboxtype\sdaps_checkbox_set_type:n
    \ExplSyntaxOff

    \myquestionbegin{name}{Option}{Attended events}
    \mysetcheckboxtype{singlechoice}
    Did you like the keynote?
    \begin{itemize}
      \item
        it was bad
          \mycheckbox{}{} ~
          \mycheckbox{}{} ~
          \mycheckbox{}{} ~
          \mycheckbox{}{} ~
          \mycheckbox{}{} ~
        it was great
      \item[\mycheckbox{}{}] I did not attend the keynote
    \end{itemize}
    \myrange{lower}{0}{bad}
    \myrange{upper}{4}{great}
    \myanswer{did not attend}
    \myquestionend{name}

Note that ``lower`` must always be the earlier checkbox. You can however assign
different values to each checkbox using the second parameter to the checkbox
command, thereby redefining the numeric value. The main different to the
``Option`` question is simply how the question will be represented in the
report.

.. _codeboxes:

Codeboxes
---------

There is experimental support for code boxes, that is not yet available using a
nice wrapper. This can be used to create QR code read fields.

.. sdaps:: Codebox question and field
    :sdapsclassic:
    :metadata:
    :preamble:
        % Prepare some stuff so that we can access the specialized commands more easily.
        \ExplSyntaxOn
        \let\myquestionbegin\sdaps_qobject_begin:nnn
        \let\mytexthbox\sdaps_textbox_hbox:nnn
        \let\myquestionend\sdaps_qobject_end:n
        \let\mysettextboxtype\sdaps_textbox_set_type:n
        % Set a global overlay with a nice icon (quite likely, you will just want
        % to place text into the hbox below rather than just placing spacing).
        \sdaps_context_set:n {
          codebox = {
            centered_text = {
              \begin{tikzpicture}[yscale=-0.1, xscale=0.1]
                \path[draw=black,fill=black,stroke=] (-1,0)
                  -- (-1,5) -- (4,5) -- (4,0) -- cycle(7,0) -- (7,5) -- (12,5) -- (12,0) -- cycle(0,1) -- (3,1) -- (3,4)
                  -- (0,4) -- cycle(8,1) -- (11,1) -- (11,4) -- (8,4) -- cycle(1,2) -- (1,3) -- (2,3) -- (2,2) -- cycle(5,2) --
                  (5,3) -- (6,3) -- (6,2) -- cycle(9,2) -- (9,3) -- (10,3) -- (10,2) -- cycle(5,4) -- (5,6) -- (2,6) -- (2,7)
                  -- (6,7) -- (6,4) -- cycle(0,6) -- (0,7) -- (1,7) -- (1,6) -- cycle(7,6) -- (7,7) -- (8,7) -- (8,6) --
                  cycle(-1,8) -- (-1,13) -- (4,13) -- (4,8) -- cycle(5,8) -- (5,13) -- (6,13) -- (6,8) -- cycle(7,8) -- (7,9)
                  -- (8,9) -- (8,10) -- (7,10) -- (7,13) -- (8,13) -- (8,11) -- (9,11) -- (9,10) -- (10,10) -- (10,9) -- (9,9)
                  -- (9,8) -- cycle(10,9) -- (12,9) -- (12,8) -- (10,8) -- cycle(0,9) -- (3,9) -- (3,12) -- (0,12) --
                  cycle(1,10) -- (1,11) -- (2,11) -- (2,10) -- cycle(11,10) -- (11,11) -- (12,11) -- (12,10) -- cycle(11,11) --
                 (10,11) -- (10,12) -- (9,12) -- (9,13) -- (12,13) -- (12,12) -- (11,12) -- cycle;
               \end{tikzpicture}
            },
          }
        }
        \ExplSyntaxOff

    \myquestionbegin{name}{Text}{This is a QR code question}
    \mysettextboxtype{codebox}

    Place barcode sticker into the box:
    % Note that we use hspace + vrule for sizing here, that is a bit weird but
    % a reasonable method of setting a size
    \mytexthbox{}{3bp}{ \hspace{8cm} \vrule width 0pt height 3cm depth 2cm }
    \myquestionend{name}

