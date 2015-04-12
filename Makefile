
PHONEY: all

sdapsbase.sty: sdapsbase.dtx sdapsbase.ins
	-rm sdapsbase.sty
	pdflatex sdapsbase.ins

sdapslayout.sty: sdapslayout.dtx sdapslayout.ins sdapsbase.sty
	-rm sdapslayout.sty
	pdflatex sdapslayout.ins

sdapsbase.pdf: sdapsbase.sty sdapsbase.dtx
	latexmk -pdf sdapsbase.dtx

sdapslayout.pdf: sdapslayout.sty sdapslayout.dtx
	latexmk -pdf sdapslayout.dtx

test.pdf: sdapslayout.sty test.tex
	latexmk -pdf test.tex
	#latexmk -xelatex test.tex


all: sdapsbase.pdf test.pdf


clean:
	-rm `cat .gitignore`

