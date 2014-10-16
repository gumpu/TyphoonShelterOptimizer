
svg_files = $(wildcard *.svg)
png_files = $(svg_files:.svg=.png)
python_files = $(wildcard *.py)

%.png : %.svg
	inkscape -b gray --export-png=$@ $< --export-width=1600

all : runlog.png tags $(png_files)

dist :
	git archive --format zip --prefix SSA/ --output ssa.zip master

runlog.csv : optimizer.py node.py shelter.py svgout.py
	python optimizer.py

runlog.png : runlog.csv
	R --vanilla < run_log_plot.r

clean : 
	-rm -f runlog.png
	-rm -f runlog.csv
	-rm -f *.svg
	-rm -f tags
	-rm -f report.txt
	-rm -f ssa.zip
	-rm -f *.png
	-rm -f Rplots.pdf

tags : $(python_files)
	ctags -R .

