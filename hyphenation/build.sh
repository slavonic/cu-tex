# create and test syllable patterns

# concatenate generated patterns with
# * special rules
# * hand-crafted long stems exceptions
# (note that we ignore exceptions)
echo "\\patterns{"         > temp.tex
cat raw_patterns.txt      >> temp.tex
cat root_patterns.txt     >> temp.tex
echo "}"                  >> temp.tex

# load paterns into temp project to generate new list of exceptions
pypatgen temp new ../data/words.txt -m 1,1
pypatgen temp import temp.tex -c
pypatgen temp compact -c
pypatgen temp test ../data/words.txt -p err_patterns.txt
rm -f cu-hyp.tex temp temp.tex

./make_hyph.py ../data/words.txt words-hyph.txt
./make_pats.py combining combiner_patterns.txt
./make_pats.py singles single_patterns.txt

# concatenate generated patterns with
# * special rules
# * hand-crafted long stems exceptions
# (note that we ignore exceptions)
echo "\\patterns{"         > temp.tex
cat raw_patterns.txt      >> temp.tex
cat combiner_patterns.txt >> temp.tex
cat root_patterns.txt     >> temp.tex
cat single_patterns.txt   >> temp.tex
echo "}"                  >> temp.tex

# load paterns into temp project to generate new list of exceptions
pypatgen temp new words-hyph.txt -m 1,2
pypatgen temp import temp.tex -c
pypatgen temp compact -c
pypatgen temp test words-hyph.txt -p err_hyph_patterns.txt
rm -f cu-hyp.tex
pypatgen temp export cu-hyp.tex

rm -f temp.tex temp words-hyph.txt 
