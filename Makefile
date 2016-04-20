SRCS = README.md \
	LICENSE \
	cu-num.sty \
	churchslavonic.sty \
	churchslavonic.tex \
	churchslavonic-en.tex \
	churchslavonic-ru.tex

DOCS = churchslavonic-en.pdf \
	churchslavonic-ru.pdf

all: package

test:
	(cd tests; make all)

clean:
	rm -f *.log *.aux *.pdf *.toc *.out comment.cut churchslavonic.zip

docs: $(DOCS)

package: churchslavonic.zip

churchslavonic.zip: $(SRCS) $(DOCS)
	rm -f $@
	zip $@ -j $^

$(DOCS): $(SRCS)

# run xelatex twice to generate toc and references
%.pdf: %.tex
	xelatex --interaction=nonstopmode $<
	xelatex --interaction=nonstopmode $<