Frequently Asked Questions
==========================

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

