sdapsclassic class
==================

This is the main class which currently should be used to create questionnaires.
It builds on top of the other packages and adds new macros and environments
which are similar to the ones from the original SDAPS LaTeX class.

Pleaes note that the environments from the sdapslayout package cannot be used
directly as using these environments will cause conflicting macro definitions.
Instead one can simply use the aliases provided in this class.

The following question types exists for your use:

* :macro:`\\singlemark`: A single range or mark question
* :macro:`\\singlemarkother`: A single range or makr question with an alternative answer in case it isn't applicable
* :macro:`\\textbox`: A large and optionally scalable textbox for freeform content
* :environ:`choicequestion`: A multiple choice question with a number of answers
* :environ:`choicegroup`: A list of multiple choice questions layed out in rows (or columns)
* :environ:`markgroup`: A list of range or mark questions layed out in rows (or columns)


Class Options
-------------

=========================== =========================
Argument                    Description
=========================== =========================
style                       The markings style to use. Either "code128", "qr"  (default: code128)
checkmode                   The mode for checkbox recognition can be any of:
                             * **checkcorrect**: check to mark, fill to correct (unmark) (default)
                             * **check**: check or fill to mark
                             * **fill**: fill to mark
globalid                    A global identifier to be printed on the document (as barcode)
globalidlabel               The label for the barcode (only code128)
no_print_questionnaire_id   Disable printing of questionnaire IDs
print_questionnaire_id      Enable printing of questionnaire IDs
=========================== =========================

Inside the environment you need to first define all possible answers with
choice macro and each question using the question macro.

Macros
------

.. macro:: \singlemark[kwargs]{question}{lower}{upper}

    A simple "mark" question, i.e. a range. The command does not currently allow adding
    an alternate answer in a way similar to the markgroup or rangearray environments.

    :arg question: The question text
    :arg lower: The text for the lower label
    :arg upper: The text for the upper label

    :kwarg text: The question text for the metadata, if set then `question` may contain fragile content.
    :kwarg lower: The lower label text for the metadata, if set then `lower` may contain fragile content.
    :kwarg upper: The upper label text for the metadata, if set then `upper` may contain fragile content.

    .. sdaps:: Simplest form of a range question
        :sdapsclassic:

        \singlemark{A range question}{lower}{upper}
        \setcounter{markcheckboxcount}{7}
        \singlemark{A range question with 7 answers}{lower}{upper}

.. macro:: \singlemarkother[kwargs]{question}{lower}{upper}{other}

    Similar to :macro:`\\singlemark` but also takes an alternative answer.

    :arg question: The question text
    :arg lower: The text for the lower label
    :arg upper: The text for the upper label
    :arg other: The text for the other label

    :kwarg text: The question text for the metadata, if set then `question` may contain fragile content.
    :kwarg lower: The lower label text for the metadata, if set then `lower` may contain fragile content.
    :kwarg upper: The upper label text for the metadata, if set then `upper` may contain fragile content.
    :kwarg other: The other label text for the metadata, if set then `other` may contain fragile content.

    .. sdaps:: A range question with an alternative answer
        :sdapsclassic:

        \singlemarkother{A range question}{lower}{upper}{other}
        \setcounter{markcheckboxcount}{7}
        \singlemarkother{A range question with 7 answers}{lower}{upper}{other}


.. macro:: \textbox*{height}{question}

    :arg *: If given, the textbox is scalable in height
    :arg height: The height of the text including a unit. If the `*` parameter is given, then this is the minimal height only
    :arg question: The question text, may not contain fragile content

    .. todo:: :macro:`\\textbox` should be able to handle an optional keyword
        argument and then allow the question text to include fragile content.

    .. sdaps:: A textbox
        :sdapsclassic:

        \textbox*{2cm}{A textbox which is 2cm high, not scaling up to the page size}
        \textbox{2cm}{A textbox which is at least 2cm high and can scale up to the page size}
        \textbox{10cm}{A textbox which is at least 10cm high sharing the rest of the page with the previous one}

Note that the SDAPS class supports rather fancy textbox handling including textboxes around
other content!

    .. warning:: The following examples are missing code for proper use! They mostly exist to show off the features but are not quite ready for easy consumption.

    .. sdaps:: Fancy textboxes, for real use additional metadata writing is required!
        :sdapsclassic:
        :metadata:

        % Prepare some stuff so that we can access the specialized commands more easily.
        \ExplSyntaxOn
        \let\sdapshbox\sdaps_textbox_hbox:nnn
        \let\sdapshstretch\sdaps_textbox_hstretch:nnnnn
        \let\sdapsvbox\sdaps_textbox_vbox:nnnn
        \ExplSyntaxOff

        \sdapshbox {} {3bp} { This hbox } should have the same baseline. And one can see that a hbox on the left edge
        is \sdapshbox{}{3bp}{ nicely aligned } with the edge. And some in a formula: $ f(x) = \frac{1}{c\,\sdapshbox{}{3bp}{box}} \sdapshstretch{}{2mm}{5mm}{40mm}{1} $

        See how even the horizontally stretching box in math mode works fine and fills up to the whole width!

        Some complex inline content:
          \sdapsvbox {} {0.6\linewidth} {3bp} {
            \begin{tabularx}{\linewidth}{l|l|X}
              adsf  lkasjd lksj flkjsfd & blub & gah \\
              \hline
              asdf & & \\
            \end{tabularx}

            This is a paragraph with more text. This is a paragraph with more text. This is a paragraph with more text. 
            This is a paragraph with more text. This is a paragraph with more text. This is a paragraph with more text. 
          }


.. macro:: \addinfo{key}{value}

    Adds a bit of metadata. This metadata will for example appear on the cover page of the report.

    :arg key: The key to set
    :arg value: The value to set the key to

    .. sdaps:: An example showing the generated metadata
        :sdapsclassic:
        :metadata:

        \addinfo{Key 1}{Value 1}
        \addinfo{Key 2}{Value 2}
        \addinfo{Key 3}{Value 3}
        \addinfo{Key 4}{Value 4}

        Almost empty document, look at the metadata to see what this is about.


Environments
------------

.. environ::
    \begin{choicequestion}[kwargs]{text}
      content
    \end{choicequestion}

    :param text: Text of the choice question. Fragile content is currently *not* supported.
    :kwarg cols: Number of columns
    :kwarg var: Variable name for this question (to be appended to context).
    :kwarg text: Replacement text for metadata

    The content should only contain :macro:`\\choiceitem`, :macro:`\\choicemulticolitem` and :macro:`\\choiceitemtext`.

    .. sdaps:: A choicequestion
        :sdapsclassic:

        \begin{choicequestion}[cols=3]{This is a choice question}
          \choiceitem{First choice}
          \choicemulticolitem{2}{Second choice with a lot of text}
          \choiceitemtext{1.2cm}{3}{Other:}
        \end{choicequestion}

    .. macro:: \choiceitem[kwargs]{text}

        A possible choice in a :environ:`choicequestion`. Will span exactly one column.

        :param text: The text for the choice. Fragile content is currently *not* supported.
        :kwarg var: Variable name for this question (to be appended to context).
        :kwarg text: Replacement text for metadata.

    .. macro:: \choicemulticolitem[kwargs]{cols}{text}

        A possible choice in a :environ:`choicequestion`. Will span exactly `cols` columns.

        :param cols: The number of columns to span.
        :param text: The text for the choice. Fragile content is currently *not* supported.
        :kwarg var: Variable name for this question (to be appended to context).
        :kwarg text: Replacement text for metadata.

    .. macro:: \choiceitemtext[kwargs]{height}{cols}{text}

        A possible freeform choice in a :environ:`choicequestion`. The text field
        will be of height `height` and it will span exactly `cols` columns.

        :param cols: The number of columns to span.
        :param text: The text for the choice. Fragile content is currently *not* supported.
        :kwarg var: Variable name for this question (to be appended to context).
        :kwarg text: Replacement text for metadata.


.. environ::
    \begin{info}
      content
    \end{info}

    A simple block to typeset important information differently.

    .. sdaps:: An info block
        :sdapsclassic:

        \begin{info}
          Just a block to write some information in, will have a line above and below.
        \end{info}


.. environ::
    \begin{markgroup}[kwargs]{text}
      content
    \end{markgroup}

    :param text: Common question for all subquestions. Fragile content is currently *not* supported
    :param kwags: Same as :environ:`rangearray`

    .. sdaps:: A group of range questions (used to be called mark)
        :sdapsclassic:

        \begin{markgroup}{A set of mark questions}
          \markline{First question}{lower}{upper}
          \markline{Second question}{lower 2}{upper 2}
        \end{markgroup}

        \begin{markgroup}{Another set of mark questions which is automatically aligned to the first}
          \markline{First question}{a}{c}
          \markline{Second question}{b}{d}
        \end{markgroup}

        \begin{markgroup}[other]{Another further set of questions with an alternative answer}
          \markline{First question}{lower}{upper}{other}
          \markline{Second question}{a}{b}{c}
        \end{markgroup}

.. todo::
    The spacing in the "other" case is not sane, we need a larger default spacing in general.



.. environ::
    \begin{choicegroup}[kwargs]{text}
      content
    \end{choicegroup}

    :param text: Common question for all subquestions. Fragile content is currently *not* supported
    :param kwags: Same as :environ:`choicearray`

    .. note:: The choicegroup environment is an alias for the :environ:`choicearray` environment. At this
        point the only difference is that the choicegroup environment correctly prints the
        header and that it uses the command aliases :macro:`\\groupaddchoice` and :macro:`\\choiceline`.

    .. macro:: \groupaddchoice[kwargs]{text}

        A possible choice inside inside the group.

        :param text: The choices (header) text.
        :kwarg text: A replacement text for the metadata, if set fragile content is
            permitted inside the `text` argument.
        :kwarg var: Variable name for this answer (to be appended to context).

    .. macro:: \choiceline[kwargs]{text}

        A single question inside the group. All choices need to be defined earlier using :macro:`\\groupaddchoice`.

        :param text: Question text.
        :kwarg text: A replacement text for the metadata, if set fragile content is
            permitted inside the `text` argument.
        :kwarg var: Variable name for this question (to be appended to context).

    .. sdaps:: Example of a choicegroup environment
        :sdapsclassic:

        \begin{choicegroup}{A group of questions}
          \groupaddchoice{Choice 1}
          \groupaddchoice{Choice 2}
          \choiceline{Question one}
          \choiceline{Question two}
        \end{choicegroup}
        
        \begin{choicegroup}{Another group of questions which is automatically aligned to the first}
          \groupaddchoice{1}
          \groupaddchoice{2}
          \choiceline{Question one}
          \choiceline{Question two}
        \end{choicegroup}

    .. sdaps:: Example of a vertical choicegroup environment also showing the "rotated" header layouter
        :sdapsclassic:

        \begin{choicegroup}[layouter=rotated,vertical]{A group of questions}
          \groupaddchoice{Choice 1}
          \groupaddchoice{Choice 2}
          \choiceline{Question one}
          \choiceline{Question two}
        \end{choicegroup}





Complex typesetting and images
------------------------------

SDAPS allows replacing the text which is exported for the metadata (i.e. what will show
up in the report). This can make sense for convenience reasons, if shortened answers
are sufficient for e.g. the report, but it also allows inserting complicated LaTeX
expressions into the document without having to fear any issues.

Apart from the advantage of having a better string in the report or similar you
also get the advantage that more TeX commands can be used in the document. Usually
environments like `verbatim` or `array` would not work inside an SDAPS environment,
but they will work if a replacement text is specified.

.. sdaps:: Example of using fragile content together with metadata text replacement
    :sdapsclassic:
    :metadata:

    \begin{choicegroup}[layouter=rotated]{A group of questions}
      \groupaddchoice[text=choice 1]{$\left( \begin{array}{cc} a & b \\ c & d \end{array} \right) + \log{\alpha}$}
      \groupaddchoice[text=choice 2]{Choice 2 -- \LaTeX}
      \choiceline[text=question 1]{\verb^Inline verbatim^}
      \choiceline[text=question 2]{
        \begin{tabularx}{0.5\linewidth}{llX}
          cell 1 & cell 2 & tabularx over half the page width fit used as the question text. This cell is the X column filling the rest of the half page.
        \end{tabularx}%
      }
      \choiceline[text=question 3]{
    \begin{verbatim}Even such things as verbatim environments work.
    However, verbatim does have some weird spacing issues (which can be partially
    solved by wrapping it into a vbox or similar).
    \end{verbatim}
      }
      \choiceline{Question 4 ends up unmodified in the metadata}
    \end{choicegroup}



Variables
---------

.. sdaps:: A choicegroup example using variables. Notice that the boxes in the metadata have variables named e.g. "flower_adam_alice"
    :sdapsclassic:
    :metadata:

    \begin{choicegroup}[var=flower]{A group of questions with variable "flower"}
      \groupaddchoice[var=alice]{Choice "alice"}
      \groupaddchoice[var=eve]{Choice "eve"}
      \choiceline[var=adam]{Question "adam"}
      \choiceline[var=bob]{Question "bob"}
    \end{choicegroup}

.. todo:: This is still somewhat broken. If the parameter is missing somewhere then
    it will not be filled in with a proper value automatically!


.. sdaps:: A markgroup example using variables. The variable is e.g. "car_alice" and the boxes have a value assigned to them. The "_dummy" is an implementation detail and should be ignored.
    :sdapsclassic:
    :metadata:

    \begin{markgroup}[var=car]{A group of questions with variable "car"}
      \markline[var=alice]{Question "alice"}{lower}{upper}
      \markline[var=bob]{Question "bob"}{lower}{upper}
    \end{markgroup}

.. todo:: Check that the _dummy should be there, pretty sure this is correct.


Preselection and overrides
--------------------------

.. todo:: Move onto separate page.


.. sdaps:: Example of a checkbox being pre-selected through the override mechanmism and the checkbox size being modified.
    :sdapsclassic:
    :metadata:

    \ExplSyntaxOn
    \sdaps_overrides_init:n{
      * = {
        flower_adam_alice = {
          draw_check=true
        },
      }
    }

    \sdaps_context_set:n{
      checkbox={
        width=8mm,
        height=4mm,
        linewidth=1.5pt,
      }
    }
    \ExplSyntaxOff
    
    \begin{choicegroup}[var=flower]{A group of questions with variable "flower"}
      \groupaddchoice[var=alice]{Choice "alice"}
      \groupaddchoice[var=eve]{Choice "eve"}
      \choiceline[var=adam]{Question "adam"}
      \choiceline[var=bob]{Question "bob"}
    \end{choicegroup}

.. warning:: The API will likely keep working, however this is rather inconvenient and helper macros not requireing ExplSyntaxOn/Off should be added.
