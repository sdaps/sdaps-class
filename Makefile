
PHONEY: all

sdapsbase.sty: sdapsbase.dtx sdapsbase.ins
	-rm sdapsbase.sty
	pdflatex sdapsbase.ins

sdapsbase.pdf: sdapsbase.sty sdapsbase.dtx
	latexmk -pdf sdapsbase.dtx

test.pdf: sdapsbase.sty test.tex
	latexmk -pdf test.tex
	#latexmk -xelatex test.tex


all: sdapsbase.pdf test.pdf


clean:
	-rm `cat .gitignore`

