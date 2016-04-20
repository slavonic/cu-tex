
all: test clean

test: test-num test-calendar test-util

test-num:
	TEXINPUTS=.:..:$$TEXINPUTS xelatex --interaction=nonstopmode cu-num-test

test-calendar:
	TEXINPUTS=.:..:$$TEXINPUTS xelatex --interaction=nonstopmode cu-calendar-test

test-util:
	TEXINPUTS=.:..:$$TEXINPUTS xelatex --interaction=nonstopmode cu-util-test

clean:
	rm -f *.aux *.log
