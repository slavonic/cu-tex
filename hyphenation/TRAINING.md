# Building hyphenation patterns for Church Slavonic

Script `train.sh` lists steps I used to generate hyphenation patterns from hyphenation dictionary [words.txt](https://??)

Quick overview of steps:

1. create two projects `cu-hyp`(base) and `cu-hypX` (auxiliary), from the same dictionary.
2. batch-train these two projects. `cu-hyp` is trained using batch specs from `specs.py`, while `cu-hypX` is trained using different specs `specsX.py`
3. replace inhibition (odd) patterns in `cu-hyp` with those from `cu-hypX`
4. compact patterns (just removes redundant patterns)
5. export patterns as `raw_patterns.txt` and export error list (in form of patterns) as `err_raw_patterns.txt`.

Rationale for using this procedure is below.

## Cross-validation of hyphenation patterns
It is easy to build TeX hyphenation patterns that cover the whole dictionary and produce no errors or produce negligible
number of errors. The real question is: how well do the patterns behave on data that was not in the training dictionary?
In other words, how well patterns generalize to the new data?

Unlike other approaches that either never tried to estimate the generalization performance, or provide only a single post-factum
testing on independent word set, I will try to tweak training parameters to maximize generalization performance.

For that I will use standard cross-validation technique. Parameter search was done manually using 3-fold cross-validation. On a final set
of training parameters 2-fold and 4-fold cross-validation was performed to confirm the numbers.

### What is cross-validation?
Here is how cross-validation works: we start with a hyphenation dictionary and split it in N equal partitions.
Then N training datasets and N testing datasets are created (they are called "folds") like follows:

* i-th testing dataset is just the i-th partition
* i-th training dataset is our dictionary with i-th partition *removed*

Now we have N folds. We take each one and use its training set to train patterns, and then test pattern performance on the fold's test words.
Since test and train sets have no common words, we can expect that the performance results on fold's test set represent real-world
generalization performance.

As a final step, we do testing for each fold and average performance of each fold. This we call "N-fold performance" of the chosen training parameters.

### To shuffle or not to shuffle?
Often, data are randomly shuffled before splitting them into fold partitions. For hyphenation we **should not** shuffle, as this would
lead to contamination of the test set. Let me explain. The hyphenation dictionary has words listed in alphabetical order. Typically
one can see many words with the same root but different suffixes listed in a row, e.g.:
```
а҆-ле-ѯа́н-дра
а҆-ле-ѯа́н-дре
а҆-ле-ѯан-дрі́й-ска-гѡ
а҆-ле-ѯа́н-дро-ви-ча
а҆-ле-ѯа́н-дро-ви-чꙋ
а҆-ле-ѯа́н-дро-ви-чѣ
а҆-ле-ѯа́н-дрꙋ
а҆-ле-ѯа́ндръ
а҆-ле-ѯа́н-дрѣ
```
If we shuffle and then split, we will almost always have variants of the same root to appear in both the test and train sets. Thus the hyphenation of the prefix will be learned from the train set, and there will be virtually no unseen prefixes in the test set. Overall this will seriously
overestimate the performance of the patterns.

Therefore I did not shuffle words before splitting into folds.

There is still an effect of "fold boundary contamination". Data partition i will have some common prefixes with the next partition and with the previous partition. Yet this can affect at most two roots, and I assumed we can ignore this effect. But note that this effect of contamination
will get stronger as the number of folds increases. And in the limit where individual partition is just a few words, the problem will be similar
to that of the shuffled list. Since I used at most 4 folds, this cross contamination effect should be negligible.

## Training parameters
Following parameters have to be defined to do the training:

1. number of pattern levels to train. In TeX hyphenation algorithm one can have as few as 1 level and as many as 9 levels. Odd levels
suggest hyphenation points (aka covering levels), even levels suppress hyphenation (aka inhibiting levels).
2. for each level decide on the range of pattern lengths. This determines the length of the patterns considered. The range is a pair of integers:
minimal length and maximal length. Thus, range=1,2 will consider only patterns of length 1 and 2.
3. selector triplet. Selector decides which patterns are accepted and which are rejected. This depends on the pattern performance.
For each pattern a statistic is computed as a pair: `num_good` (number of "good" decisions the pattern made on the training set) and
`num_bad` (number of "bad" decisions the pattern made on the training set). The pattern is accepted whenever
`num_good * good_weight - num_bad * bad_weights >= threshold`. The triplet of integer numbers `(good_weight, bad_weight, threshold)` is the
selector.

Important to note that the `threshold` parameter depends on the dataset size. As the dictionary grows, `threshold` must be scaled proportionally
in order for the selector to keep its selectivity at the same level. This is important for cross-validation, where the training dataset is smaller
than the full dataset. Therefore, when applying learned parameters to a new dataset this has to be kept in mind. Note also that large
values of `threshold` are most susceptible to this scaling effect.

Interestingly, in our case this scaling effect can be completely ignored, because we use only selectors where `threshold` value is small
- and we use threshold value of 1 for all corss-validation dataset.

## Experience of parameter selection for best generalization

Experimenting with different number of levels and different range of pattern lengths, I found that

1. There is no advantage in having more than two pattern levels. Of course, we do need inhibiting patterns. Therefore, the best
   choice of the number of levels is exactly 2!
2. Single-letter hyphenation patterns are useless. First, the algorithm finds just few such patterns. Second, they seem to give rise to
   many false hyphenations, so that the overall effect is negative.
3. Single-letter inhibiting patterns are very useful. They allow the algorithm to learn places where hyphenation never happens (i.e. before a
   combining symbol)
4. Long patterns are bad. Using patterns longer than 4 degrades performance. I have no good explanation for this.
5. Selector can be made more *selective* by either raising `threshold` or raising `bad_weight`. The empirical observation is that patterns
   that keep `threshold` at minimum value (1) and control selectivity via `bad_weight` parameter only, generalize better.

## Mix-and-match inhibition levels
In our two-level pattern training configuration, the first level (level 1) is covering level, and second level (level 2) is inhibiting level.

To minimize generation of false hyphen prediction we need to strive for:

1. covering level to produce minimal amount of bad suggestions
2. inhibition level to be robust to cover as many as possible patterns where hyphenation is forbidden

within a single pattern training session it is impossible to satisfy both requirements:
if we make selector more selective, we then accept only "good" patterns that produce just few false hyphenation points. On such a thin
dataset it is impossible to build a good set of inhibition patterns. And, conversely, if we want to build a good inhibition level
we need to give it an input with many false hits, which means that we need to make hyphenation level more lax.

The idea of mixing-and-matching inhibition levels tries to overcome this limitation. To do this, we train two independent pattern sets - base and auxiliary.
Base pattern set we train with highly-selective criteria in order to get good hyphenation patterns. We do not care much for the inhibition level in the base.

The  auxiliary pattern set is trained
with very lax selector for covering level and very selective one for the inhibition level. We then construct the final pattern set
by replacing inhibition level in the base with the inhibition level from the auxiliary one! In practice, this technique is very effective,
shaving off 30-50% of errors.

## Cross-validation scripts

Scripts that were used for cross-validation are:

* `cv2.sh` - does two-fold cross-validation
* `cv3.sh` - does three-fold cross-validation
* `cv4.sh` - does four-fold cross-validation

See corresponding `cv-?.log` files for the results. Summary is below (note that total weighted number of hyphens in the
dictionary is 40468 - it is used to compute percentages below).

|  script  | total number of missed | total number of false | percent missed | percent false |
|----------|------------------------|-----------------------|----------------|---------------|
|  `cv2`   |  4222                  |  1825                 |  10.4          | 4.5           |
|  `cv3`   |  3508                  |  1680                 |  8.7           | 4.1           |
|  `cv4`   |  3566                  |  1687                 |  8.8           | 4.2           |

Number of words in the dictionary is 17525. This gives on average 2 hyphens per word. Therefore, 75% of new words
will be hyphenated correctly. Other 25% of new words will have some deficiency - either a missing hyphen or an incorrectly
suggested hyphen.

Since hyphenation algorithm selects a single hyphen from a word, the per-hyphen performance statistics better represent the
probability of error than word-level statistics.

Since our dictionary covers 90% of words in the corpus (and since all words in the dictionary will be 100% correct due to the
exception list), the overall expected performance on the text is 0.87% probability of missing a hyphen, and 0.41% probability
of incorrect hyphenation.

Only incorrect hyphenation is really important, as it easily catches the eye of the reader (whereas missed hyphenation
just makes TeX pick another hyphenation point - just a less optimal one).
Assuming that we will need at most 10 hyphenations per page, the risk of getting an incorrect hyphenation is approximately
4% per page.
