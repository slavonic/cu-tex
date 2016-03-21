wc ../data/words.txt
split -l 5837 ../data/words.txt w3
wc w3a?
cat w3aa w3ab > w3a-ab
cat w3aa w3ac > w3a-ac
cat w3ab w3ac > w3a-bc
wc w3a-??

rm -f cv3-?? cv3-??X
#
pypatgen cv3-bc  new w3a-bc --margins 1,1
pypatgen cv3-bcX new w3a-bc --margins 1,1
pypatgen cv3-ac  new w3a-ac --margins 1,1
pypatgen cv3-acX new w3a-ac --margins 1,1
pypatgen cv3-ab  new w3a-ab --margins 1,1
pypatgen cv3-abX new w3a-ab --margins 1,1
#
pypatgen cv3-bc  batchtrain specs.py
pypatgen cv3-bcX batchtrain specsX.py
pypatgen cv3-ac  batchtrain specs.py
pypatgen cv3-acX batchtrain specsX.py
pypatgen cv3-ab  batchtrain specs.py
pypatgen cv3-abX batchtrain specsX.py
#
pypatgen cv3-bc swap cv3-bcX -c
pypatgen cv3-ac swap cv3-acX -c
pypatgen cv3-ab swap cv3-abX -c
#
pypatgen cv3-bc compact -c
pypatgen cv3-ac compact -c
pypatgen cv3-ab compact -c
#
pypatgen cv3-bc test w3aa -e err3-a
pypatgen cv3-ac test w3ab -e err3-b
pypatgen cv3-ab test w3ac -e err3-c
