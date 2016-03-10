wc ../data/words.txt
cat ../data/words.txt > w

rm -f cu-hyp cu-hypX
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
pypatgen cu-hyp test w -e err
#
pypatgen cu-hyp export cu-hyp.tex

