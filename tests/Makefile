
all: test clean

test:
	TEXINPUTS=.:..:$$TEXINPUTS xelatex --interaction=nonstopmode cu-num-test


clean:
	rm -f *.aux *.log
