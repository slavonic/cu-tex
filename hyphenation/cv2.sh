wc ../data/words.txt
rm -f wc2a?
split -l 8762 ../data/words.txt w2
wc w2a?

rm -f cv2-? cv2-??
#
pypatgen cv2-a  new w2aa --margins 1,1
pypatgen cv2-aX new w2aa --margins 1,1
pypatgen cv2-b  new w2ab --margins 1,1
pypatgen cv2-bX new w2ab --margins 1,1
#
pypatgen cv2-a  batchtrain specs.py
pypatgen cv2-aX batchtrain specsX.py
pypatgen cv2-b  batchtrain specs.py
pypatgen cv2-bX batchtrain specsX.py
#
pypatgen cv2-a swap cv2-aX -c
pypatgen cv2-b swap cv2-bX -c
#
pypatgen cv2-a compact -c
pypatgen cv2-b compact -c
#
pypatgen cv2-b test w2aa -e err2-a
pypatgen cv2-a test w2ab -e err2-b

rm -f wc2a?
rm -f cv2-? cv2-??
