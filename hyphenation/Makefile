WORDS_SYL = ../data/words.txt

all: hyph-cu.tex

clean:
	rm -f cu-syl cu-sylX cu-syl.tex
	rm -f temp.tex temp words-hyph.txt
	rm -f temp words-hyph.txt words-hyph-expanded.txt
	rm -f cu-hyph.tex cu-hyph-expanded.tex
	rm -f *.err
	rm -f syl_patt.txt syl_patt_errors.txt
	rm -f combiner_patterns.txt
	rm -f single_patterns.txt

syl_patt.txt syl_patt.err: $(WORDS_SYL)
	echo 'Training RAW syllable patterns'
	wc $(WORDS_SYL)  # just to show how many words are there
	#
	pypatgen cu-syl  new $(WORDS_SYL) --margins 1,1
	pypatgen cu-sylX new $(WORDS_SYL) --margins 1,1
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
	pypatgen cu-syl test $(WORDS_SYL) -p syl_patt.err
	#
	pypatgen cu-syl export cu-syl.tex -p syl_patt.txt
	rm -f cu-syl cu-sylX cu-syl.tex

syl-cu.tex: syl_patt.txt root_patterns.txt $(WORDS_SYL)
	echo 'Making syllable patterns (by adding root and combiner patterns)'
	echo "\\patterns{"         > temp.tex
	cat syl_patt.txt          >> temp.tex
	cat combiner_patterns.txt >> temp.tex
	cat root_patterns.txt     >> temp.tex
	echo "}"                  >> temp.tex
	# load paterns into temp project to dedup and get list of exceptions
	rm -f syl-cu.* temp
	pypatgen temp new $(WORDS_SYL) -m 1,1
	pypatgen temp import temp.tex -c
	pypatgen temp compact -c
	pypatgen temp test $(WORDS_SYL) -p syl-cu.err
	pypatgen temp export syl-cu.tex -p patterns.txt

words-hyph.txt: $(WORDS_SYL)
	./make_hyph.py $(WORDS_SYL) words-hyph.txt

combiner_patterns.txt single_patterns.txt: make_pats.py
	./make_pats.py combining combiner_patterns.txt
	./make_pats.py singles single_patterns.txt

cu-hyph.tex: syl_patt.txt \
		combiner_patterns.txt root_patterns.txt single_patterns.txt \
		words-hyph.txt
	rm -f temp cu-hyph.*
	echo "\\patterns{"         > temp.tex
	cat syl_patt.txt          >> temp.tex
	cat combiner_patterns.txt >> temp.tex
	cat root_patterns.txt     >> temp.tex
	cat single_patterns.txt   >> temp.tex
	echo "}"                  >> temp.tex
	# load paterns into temp project to dedup and get list of exceptions
	pypatgen temp new words-hyph.txt -m 1,2
	pypatgen temp import temp.tex -c
	pypatgen temp compact -c
	pypatgen temp test words-hyph.txt -p cu-hyph.err
	pypatgen temp export cu-hyph.tex

words-hyph-expanded.txt: expand.py words-hyph.txt
	echo 'Generating expanded hyphenation dictionary'
	./expand.py words-hyph.txt words-hyph-expanded.txt

cu-hyph-expanded.tex: cu-hyph.tex \
			words-hyph.txt words-hyph-expanded.txt
	echo 'Generating expanded version of patterns'
	rm -f temp cu-hyph-expanded.*
	./expand.py cu-hyph.tex temp.tex
	pypatgen temp new words-hyph-expanded.txt -m 1,2
	pypatgen temp import temp.tex -c
	pypatgen temp compact -c
	pypatgen temp test words-hyph.txt
	pypatgen temp test words-hyph-expanded.txt -p cu-hyph-expanded.err
	pypatgen temp export cu-hyph-expanded.tex

# remove parasites
hyph-cu.tex: cu-hyph-expanded.tex parasitic_patterns.txt
	echo 'Removing parasites and building final hyphenation patterns'
	rm -f temp hyph-cu.*
	awk 'NR==FNR{a[$$0];next} !($$0 in a)' \
		parasitic_patterns.txt cu-hyph-expanded.tex > temp.tex
	# test performance after removal of parasites
	pypatgen temp new words-hyph-expanded.txt -m 1,2
	pypatgen temp import temp.tex -c
	pypatgen temp compact -c
	pypatgen temp test words-hyph.txt
	pypatgen temp test words-hyph-expanded.txt -p hyph-cu.err
	pypatgen temp export hyph-cu.tex
