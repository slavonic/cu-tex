#!/bin/bash

./make_hyph.py ../data/words.txt words-hyph.txt

./expand.py cu-hyp.tex cu-hyp-expanded.tex
./expand.py words-hyph.txt words-hyph-expanded.txt

# lets de-duplicate by loading and testing

rm -f temp cu-hyp-expanded2.tex
pypatgen temp new words-hyph-expanded.txt -m 1,2
pypatgen temp import cu-hyp-expanded.tex -c
pypatgen temp compact -c
pypatgen temp test words-hyph.txt
pypatgen temp test words-hyph-expanded.txt -p err_expanded.txt
pypatgen temp export cu-hyp-expanded2.tex

rm -f temp words-hyph.txt words-hyph-expanded.txt
