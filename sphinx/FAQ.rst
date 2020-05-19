Frequently Asked Questions
==========================

Numeric field input
-------------------

Sometimes the input of longer numbers is required. Freeform text cannot be used
so that other methods are necessary. The method presented here is a field of
checkboxes, but further options may exist depending on the solution:

* Use of a unique questionnaire ID and be careful when handing out the questionnaire
* :ref:`Codeboxes`, i.e. text fields where a barcode sticker is placed

In this example, each digit of an 8 digit number is asked for using an
:environ:`optiongroup` environment.

.. sdaps:: Using optiongroup to input longer numbers
    :sdapsclassic:

    \begin{optiongroup}[vertical]{Please enter the 8 digit number}
      % Set the value as it would be 1 based otherwise, so we can just
      % use it directly from the data export
      \choice[val=0]{0}
      \choice[val=1]{1}
      \choice[val=2]{2}
      \choice[val=3]{3}
      \choice[val=4]{4}
      \choice[val=5]{5}
      \choice[val=6]{6}
      \choice[val=7]{7}
      \choice[val=8]{8}
      \choice[val=9]{9}
      \question[text=d1]{$\bigsqcup$}
      \question[text=d2]{$\bigsqcup$}
      \question[text=d3]{$\bigsqcup$}
      \question[text=d4]{$\bigsqcup$}
      \question[text=d5]{$\bigsqcup$}
      \question[text=d6]{$\bigsqcup$}
      \question[text=d7]{$\bigsqcup$}
      \question[text=d8]{$\bigsqcup$}
    \end{optiongroup}


How can one use images?
-----------------------

The normal LaTeX commands will work as usual. As the image needs to be
available during and after the `setup` step of SDAPS extra steps will be
required though. The basic problem is that the given LaTeX file is copied
into a new directory and the images may not be available then. The following
ways exist to deal with this:

 1. Copy all images by passing `--add` for each image
 2. Place all images into a directory and use `--add` on the directory

The second option is a good strategy if you have more images. In the example
below a directory called `images` is used which has one file called `sdaps.png`.
The `\\graphicspath` command is used so that the image can be refered to by its
filename rather than the full relative path.

.. sdaps:: Using `graphicx` together with `\\graphicspath` to place images into a subdirectory
    :sdapsclassic:
    :preamble:
         \usepackage{graphicx}
         % Do not add a leading ./ as that will cause issues under some conditions!
         \graphicspath{{images/}}

    The SDAPS logo for the website is \raisebox{-0.8cm}{\includegraphics[width=2cm]{sdaps.png}}.

With that done, you need to run the following to setup the project

.. code-block:: shell

    $ sdaps setup tex PROJECT_DIR questionnaire.tex --add images

