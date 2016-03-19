./make_hyph.py ../data/words.txt words-hyph.txt
cp ../data/words.txt words-hyph.txt

wc words-hyph.txt

rm -f cu-hyp cu-hypX cu-hyp.tex
#
pypatgen cu-hyp  new words-hyph.txt --margins 1,1
pypatgen cu-hypX new words-hyph.txt --margins 1,1
#
pypatgen cu-hyp  batchtrain specs.py
pypatgen cu-hypX batchtrain specsX.py
#
pypatgen cu-hyp swap cu-hypX -c
#
pypatgen cu-hyp compact -c
#
# following test is useless - on the test data!
# but it creates error log in the form of patterns
pypatgen cu-hyp test words-hyph.txt -p err_raw_patterns.txt
#
pypatgen cu-hyp export cu-hyp.tex -p raw_patterns.txt
rm -f cu-hyp cu-hypX cu-hyp.tex words-hyph.txt

