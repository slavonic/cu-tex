cp ../data/words.txt words-syl.txt

wc words-syl.txt

rm -f cu-syl cu-sylX cu-syl.tex
#
pypatgen cu-syl  new words-syl.txt --margins 1,1
pypatgen cu-sylX new words-syl.txt --margins 1,1
#
pypatgen cu-syl  batchtrain specs.py
pypatgen cu-sylX batchtrain specsX.py
#
pypatgen cu-syl swap cu-sylX -c
#
pypatgen cu-syl compact -c
#
# following test is useless - on the test data!
# but it creates error log in the form of patterns
pypatgen cu-syl test words-syl.txt -p err_raw_patterns.txt
#
pypatgen cu-syl export cu-syl.tex -p raw_patterns.txt
rm -f cu-syl cu-sylX cu-syl.tex words-syl.txt

