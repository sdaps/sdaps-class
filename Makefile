
PHONEY: all

sdapsbase.sty: sdapsbase.dtx sdapsbase.ins
	-rm sdapsbase.sty
	pdflatex sdapsbase.ins

sdapslayout.sty: sdapslayout.dtx sdapslayout.ins sdapsbase.sty
	-rm sdapslayout.sty
	pdflatex sdapslayout.ins

sdapspdf.sty: sdapspdf.dtx sdapspdf.ins sdapsbase.sty
	-rm sdapspdf.sty
	pdflatex sdapspdf.ins

sdapsbase.pdf: sdapsbase.sty sdapsbase.dtx
	latexmk -pdf sdapsbase.dtx

sdapslayout.pdf: sdapslayout.sty sdapslayout.dtx
	latexmk -pdf sdapslayout.dtx

sdapspdf.pdf: sdapspdf.sty sdapspdf.dtx
	latexmk -pdf sdapspdf.dtx

test.pdf: sdapslayout.sty sdapspdf.sty test.tex
	latexmk -pdf test.tex
	#latexmk -xelatex test.tex


all: sdapsbase.pdf sdapslayout.pdf sdapspdf.pdf test.pdf


clean:
	-rm `cat .gitignore`

