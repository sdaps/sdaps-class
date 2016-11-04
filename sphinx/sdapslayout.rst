sdapslayout package
===================

This package provides a set of more complex layouting options on top of the
sdapsarray package. The following environments are provided:

 * choicearray
 * rangearray

The rangearray is not quite as powerful, as it does not expose some of the
sdapsarray options to the user. Note that much more complex custom layouts can
be created directly with sdapsarray.

.. _choicearray:

choicearray environment
-----------------------

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

The following optional keyword parameters can be passed to the
environment. These keyword parameters default to the values provided in the
SDAPS environment and can for example be modified globally for the document.

.. todo::
     Right now all arguments can be overriden, this should not be the case. It
     would be correct if the variable name is loaded from the kwargs, and then
     the defaults for align and horizontal/vertical should be applied

============  =========================
Argument      Description
============  =========================
align         named alignment group, by default \env{choicearay} environments are aligned if the layouter and orientation match
horizontal    set horizontal mode where each question is one row (default)
layouter      set the sdapsarray layouter (e.g. rotated for rotated column headers)
text          override the normal header (not useful currently!)
var           if set appends the variable name to the newly created scope ('_' separator is added automatically)
vertical      set vertical mode where each question is one column
============  =========================

Inside the environment you need to first define all possible answers with
choice macro and each question using the question macro.

