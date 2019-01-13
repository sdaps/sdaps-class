sdapslayout package
===================

This package provides a set of more complex layouting options on top of the
sdapsarray package. The following environments are provided:

* :environ:`choicearray`
* :environ:`rangearray`

The rangearray is not quite as powerful, as it does not expose some of the
sdapsarray options to the user. Note that much more complex custom layouts can
be created directly with sdapsarray.

.. warning:: The documentation here is currently incomplete! Pleases refer to the sdapsclassic :environ:`choicegroup` and :environ:`markgroup` documentation!

.. environ::
    \begin{choicearray}[kwargs]{text}
    \end{choicearray}

    :param text: Text header text for the group (metadata only as of now).

    The following optional keyword parameters can be passed to the
    environment. These keyword parameters default to the values provided in the
    SDAPS context and can for example be modified globally for the document.

    :kwarg align:         named alignment group, by default \env{choicearay} environments are aligned if the layouter and orientation match
    :kwarg noalign:       disable alignment (same as setting ``align`` to an empty value)
    :kwarg horizontal:    set horizontal mode where each question is one row (default)
    :kwarg layouter:      set the sdapsarray layouter (e.g. rotated for rotated column headers)
    :kwarg angle:         set the angle of the column headers when in rotated mode
    :kwarg text:          override the normal header (not useful currently!)
    :kwarg var:           if set appends the variable name to the newly created scope ('_' separator is added automatically)
    :kwarg vertical:      set vertical mode where each question is one column
    :kwarg type:          the question type "multichoice" or "singlechoice"
    :kwarg multichoice:   switch to multichoice "Choice" question mode
    :kwarg singlechoice:  switch to singlechoice "Option" question mode


    The choicearray environment represents a tabular layout for a set of multiple
    choice questions which have the same possible answers. A new header is created
    in the metadata to group the questions.

    .. warning:: The header is currently *not shown* in the PDF and it cannot
        contain fragile content due to implementation constraints! This is an issue
        with the class which will be fixed. The exact final behaviour is not yet
        specified.

    .. sdaps:: Example of a choicearray environment

        \begin{choicearray}[layouter=rotated]{A group of questions}
          \choice{Choice 1}
          \choice{Choice 2}
          \question{Question one}
          \question{Question two}
        \end{choicearray}

    .. sdaps:: Example of a vertical choicearray environment

        \begin{choicearray}[layouter=rotated,vertical]{A group of questions}
          \choice{Choice 1}
          \choice{Choice 2}
          \question{Question one}
          \question{Question two}
        \end{choicearray}

    .. todo::
         Right now all arguments can be overriden, this should not be the case. It
         would be correct if the variable name is loaded from the kwargs, and then
         the defaults for align and horizontal/vertical should be applied


    Inside the environment you need to first define all possible answers with
    choice macro and each question using the question macro.


.. environ::
    \begin{rangearray}[]{}
    \end{rangearray}

    .. todo:: Uh, document this.
