rm -f temp

# concatenate generated patterns with
# * special rules
# * hand-crafted long stems exceptions
# (note that we ignore exceptions)
echo "\\patterns{" > cu-hyp.tex
cat cu-hyp-patterns.txt >> cu-hyp.tex
cat cu-hyph-extra.txt >> cu-hyp.tex
cat cu-hyph-extra3.txt >> cu-hyp.tex
echo "}" >> cu-hyp.tex

# load paterns into temp project to generate new list of exceptions
pypatgen temp new ../data/words.txt -m 1,1
pypatgen temp import cu-hyp.tex -c
pypatgen temp test ../data/words.txt -p err_patterns.txt
rm -f cu-hyp.tex
pypatgen temp export cu-hyp.tex
