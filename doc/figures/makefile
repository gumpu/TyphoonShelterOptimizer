
svg_files = $(wildcard *.svg)
png_files = $(svg_files:.svg=.png)

%.png : %.svg
	inkscape -b gray --export-png=$@ $< --export-width=600

all : $(png_files)


