wc ../data/words.txt
cat ../data/words.txt > w

rm -f cu-hyp cu-hypX cu-hyp.tex
#
pypatgen cu-hyp  new w --margins 1,1
pypatgen cu-hypX new w --margins 1,1
#
pypatgen cu-hyp  batchtrain specs.py
pypatgen cu-hypX batchtrain specsX.py
#
pypatgen cu-hyp swap cu-hypX -c
#
pypatgen cu-hyp compact -c
#
# folowing test is useless - on the test data!
# but it creates error log in the form of patterns
pypatgen cu-hyp test w -e err -p err_patterns.txt
#
pypatgen cu-hyp export cu-hyp.tex

