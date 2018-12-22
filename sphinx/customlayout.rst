Creating custom layouts using base commands
===========================================

Usually the pre-defined layouts that SDAPS provides are sufficent. However,
there may be special cases that need more customization. Such customization is
possible, but it does require a more in depth understanding of LaTeX and
the SDAPS packages.

If you do this, please make sure to properly test the output. The easiest way
of such testing is to use the ``anotate`` command that SDAPS provides, as it
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
    \let\mytextbox\sdaps_qobject_end:n
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
    \let\mytextbox\sdaps_qobject_end:n
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
    \let\mytextbox\sdaps_qobject_end:n
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


