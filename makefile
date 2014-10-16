
svg_files = $(wildcard *.svg)
png_files = $(svg_files:.svg=.png)

%.png : %.svg
	inkscape -b gray --export-png=$@ $< --export-width=1600

all : runlog.png p.png tags $(png_files)

dist :
	git archive --format zip --prefix SSA/ --output ssa.zip master

problem.txt : construct_problem.py RealData/existing_shelters.csv RealData/new_locations.csv RealData/village_centers.csv
	python construct_problem.py

p.svg runlog.csv : sop.py problem.txt problem_1.txt node.py shelter.py svgout.py
	python sop.py

runlog.png : runlog.csv
	R --vanilla < run_log_plot.r

clean : 
	-rm -f problem.txt
	-rm -f runlog.png
	-rm -f runlog.csv
	-rm -f p.svg
	-rm -f tags
	-rm -f report.txt
	-rm -f ssa.zip
	-rm -f p.png

tags : sop.py
	ctags -R .

