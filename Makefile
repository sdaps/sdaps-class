
all: sdapsbase.pdf sdapslayout.pdf sdapspdf.pdf test.pdf sdapsclassic.pdf testclassic.pdf

sdapsbase.sty: sdapsbase.dtx sdapsbase.ins
	-rm sdapsbase.sty
	pdflatex sdapsbase.ins

sdapslayout.sty: sdapslayout.dtx sdapslayout.ins sdapsbase.sty
	-rm sdapslayout.sty
	pdflatex sdapslayout.ins

sdapsclassic.cls: sdapsclassic.dtx sdapsbase.sty
	-rm sdapsclassic.cls
	pdflatex sdapsclassic.ins

sdapspdf.sty: sdapspdf.dtx sdapspdf.ins sdapsbase.sty
	-rm sdapspdf.sty
	pdflatex sdapspdf.ins

sdapsbase.pdf: sdapsbase.sty sdapsbase.dtx
	latexmk -pdf sdapsbase.dtx

sdapslayout.pdf: sdapslayout.sty sdapslayout.dtx
	latexmk -pdf sdapslayout.dtx

sdapspdf.pdf: sdapspdf.sty sdapspdf.dtx
	latexmk -pdf sdapspdf.dtx

sdapsclassic.pdf: sdapsbase.sty sdapsclassic.cls
	latexmk -pdf sdapsclassic.dtx

test.pdf: sdapslayout.sty sdapspdf.sty test.tex
	latexmk -pdf test.tex
	#latexmk -xelatex test.tex

testclassic.pdf: sdapsclassic.cls testclassic.tex
	latexmk -pdf testclassic.tex


clean:
	-rm `cat .gitignore`

