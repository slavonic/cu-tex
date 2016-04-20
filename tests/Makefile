
all: test clean

test: test-num test-calendar test-util

test-num:
	TEXINPUTS=.:..:: xelatex --interaction=nonstopmode cu-num-test

test-calendar:
	TEXINPUTS=.:..:: xelatex --interaction=nonstopmode cu-calendar-test

test-util:
	TEXINPUTS=.:..:: xelatex --interaction=nonstopmode cu-util-test

clean:
	rm -f *.aux *.log
