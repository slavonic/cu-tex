wc ../data/words.txt
split -l 4381 ../data/words.txt w4
wc w4a?
cat w4ab w4ac w4ad > w4a-bcd
cat w4aa w4ac w4ad > w4a-acd
cat w4aa w4ab w4ad > w4a-abd
cat w4aa w4ab w4ac > w4a-abc
wc w4a-???

rm -f cv4-??? cv4-???X
#
pypatgen cv4-bcd  new w4a-bcd --margins 1,1
pypatgen cv4-bcdX new w4a-bcd --margins 1,1
pypatgen cv4-acd  new w4a-acd --margins 1,1
pypatgen cv4-acdX new w4a-acd --margins 1,1
pypatgen cv4-abd  new w4a-abd --margins 1,1
pypatgen cv4-abdX new w4a-abd --margins 1,1
pypatgen cv4-abc  new w4a-abc --margins 1,1
pypatgen cv4-abcX new w4a-abc --margins 1,1
#
pypatgen cv4-bcd  batchtrain specs.py
pypatgen cv4-bcdX batchtrain specsX.py
pypatgen cv4-acd  batchtrain specs.py
pypatgen cv4-acdX batchtrain specsX.py
pypatgen cv4-abd  batchtrain specs.py
pypatgen cv4-abdX batchtrain specsX.py
pypatgen cv4-abc  batchtrain specs.py
pypatgen cv4-abcX batchtrain specsX.py
#
pypatgen cv4-bcd swap cv4-bcdX -c
pypatgen cv4-acd swap cv4-acdX -c
pypatgen cv4-abd swap cv4-abdX -c
pypatgen cv4-abc swap cv4-abcX -c
#
pypatgen cv4-bcd compact -c
pypatgen cv4-acd compact -c
pypatgen cv4-abd compact -c
pypatgen cv4-abc compact -c
#
pypatgen cv4-bcd test w4aa -e err4-a
pypatgen cv4-acd test w4ab -e err4-b
pypatgen cv4-abd test w4ac -e err4-c
pypatgen cv4-abc test w4ad -e err4-d
