
all: test clean

test: test-num test-calendar

test-num:
	TEXINPUTS=.:..:$$TEXINPUTS xelatex --interaction=nonstopmode cu-num-test

test-calendar:
	TEXINPUTS=.:..:$$TEXINPUTS xelatex --interaction=nonstopmode cu-calendar-test

clean:
	rm -f *.aux *.log
