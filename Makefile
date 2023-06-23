SRCS = README.ctan \
	LICENSE \
	cu-num.sty \
	cu-calendar.sty \
	cu-util.sty \
	cu-kinovar.sty \
	cu-kruk.sty \
	churchslavonic.sty \
	churchslavonic.tex \
	churchslavonic-en.tex \
	churchslavonic-ru.tex \
	gloss-churchslavonic.ldf

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
	rm -rf /tmp/churchslavonic
	mkdir /tmp/churchslavonic
	cp $^ /tmp/churchslavonic
	mv /tmp/churchslavonic/README.ctan /tmp/churchslavonic/README
	rm -f $@
	(cd /tmp; zip $@ -r churchslavonic)
	mv /tmp/churchslavonic.zip .
	rm -rf /tmp/churchslavonic

$(DOCS): $(SRCS)

# run xelatex twice to generate toc and references
%.pdf: %.tex
	lualatex --interaction=nonstopmode $<
	lualatex --interaction=nonstopmode $<
