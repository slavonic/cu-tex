# Creating hyphenation patterns for Church Slavonic

## Requirements

- Python installed (Python 3 is recommended as it is noticeably faster)
- `pypatgen` version 2.9 or better

## Quick Start
To build TeX file with hyphenation patterns and hyphenations exceptions, just do this:
```
make clean
make
```
Result should be a file `hyph-cu.tex`.

When one of the input changes, use `make` to rebuild the result.

To build CTAN package (ZIP file `hyphen-churchslavonic.zip` ready to be uploaded to [CTAN](http://www.ctan.org/upload/)), do:
```
make ctan
```

Explanations of (some) files in this directory (note that some of the mentioned files are created by `make` command):
* `Makefile` - does all the dirty work
* `hyph-cu.tex` - the ultimate result
* `hyph-cu.err` - hyphenation exceptions in pattern format
* `cv2.sh`, `cv3.sh`, and `cv4.sh` - scripts used to do 2-fold, 3-fold, and 4-fold cross-validation of trained syllable
   patterns
* `combiner_patterns.txt` - contains TeX patterns inhibiting hyphenation before a combining symbol (like accent).
   These patterns are generated with `make_pats.py` script. If you want to change it, change script, not `*.txt`.
* `root_patterns.txt` - hand-crafted patterns for some common roots that raw patterns do not cover. 
* `single_patterns.txt` - patterns that inhibit hyphenation before last character and after the first character (note that
  because of the accents setting `lefthyphenmin=1` and `righthyphenmin=2` is not sufficient.
* `specs.py`, `specsX.py` - specifications for training syllable patterns.
* `syl_patt.txt` - syllable patterns, learned from syllable dictionary.
* `syl_patt.err` - errors that syllable patterns make on the syllable dictionary.
* `words-hyph.txt` - hyphenation dictionary
* `words-hyph-expanded.txt` - expanded hyphenation dictionary
* `make_hyph.py` - script to generate hyphenation dictionary from syllable dictionary. Hyphenation dictionary differs
  from syllable dictionary because hyphenation is not allowed before a last vowel (even if it forms a syllable), and
  generally (with some exceptions) not allowed after a single vowel.
* `make_pats.py` - script to generate `combiner_patterns.txt` and `single_patterns.txt`.
* `expand.py` - does recursive NFC<->NFD expansion of characters
* `cu_hyph.tex` - TeX hyphenation patterns (in NFC form, unexpanded)
* `cu_hyph_expanded.tex` - expanded patterns, have some parasites


## Long Story
In Church Slavonic words are hyphenated on the syllable boundary. Syllable boundaries are determined
on the basis of complex morphological rules given in the syllable dictionary. No hyphenation is allowed
before a single-letter syllable at the end of a word and no hyphenation is allowed after a single-letter syllable at the beginning of a word **with some exceptions** (See below).
Note that by a single-letter syllable we mean such a syllable that has a single letter (always a vowel), optionally followed by one
or more combining marks (accents); by spelling convention, any vowel at the beginning of a word will always have a breathing mark.

We create TeX hyphenation patterns in the following stages

1. Create syllable patterns. We do this by training on a syllable dictionary [words.txt](../data/words.txt) and adding
   some hand-crafted patterns to cover common roots where learned patterns fail. Specifically:

    - Use the hyphenation dictionary to automatically generate patterns. 
      Since dictionary uses [Unicode Normal Form C](http://unicode.org/reports/tr15/), all patterns will also be in this form.

    - Analyze errors that patterns make on the hyphenation dictionary and add (long) patterns that cover offending stems. This
      essentially allows one to move some errors out of the exception list into patterns, hoping that the new pattern will
      cover all word forms (not just forms seen within the training dictionary).

    - Add special patterns that ensure that no hyphenation happens before a combining character. Since Church Slavonic
      uses a rich set of diacritical marks, we do not rely on step 1 to find all of these places, and just add these rules 
      explicitly<sup>[1][1]</sup>
      
   This step is performed by
   ```
   make cu-hyph.tex
   ```

2. Add patterns to suppress hyphenation after the first letter and before the last letter. Note that we cannot rely here on
   TeX mechanism of `lefthyphenmin` and `righthyphenmin` because (i) TeX also counts accents and breathing marks as characters when counting
   "letters", and (ii) there are exceptional cases when hyphenation after a single letter at the beginning of a word is allowed. To achieve our goal we
   generate a list of all vowels and then list all vowels with all possible (and sometimes impossible) combining accents.
   From this list we create inhibiting patterns for word prefixes and suffixes.
   
   Since Church Slavonic allows hyphenation after some vowels at the beginning of a word, we remove
corresponding inhibiting prefix rules:
   
    - Hyphenation is allowed after a leading syllable ѿ (OT), ѹ (UK), and ѡ (OMEGA)
   
   At this stage we also generate the TeX list of hyphenation exceptions.
   
   ```
   make cu-hyph.tex
   ```
   
3. Expand patterns and exception list by replacing each character with its Normal Form D. Note that for robustness
   we create all combinations of D and C forms for every character that has these different forms. This is different
   than just converting each pattern and exception to Normal Form D. To the built-in Unicode combining rules we add 
   the following two extra rules:
   
    - U+0479 <-> U1C82 U0443 (Sharp-O decomposition of UK) - this will be included in the upcoming revision of Unicode, but
      current engines do not know this yet
    - U+047D <-> U+A64D U+0486 U+0311 (omega with veliky apostrof) - this symbol is incorrectly marked as not decomposable
      in Unicode

    ```
    make cy-hyph-expanded.tex
    ```

4. Remove some patterns that do not do any good, but after pattern expansion actually do some harm (we call them "parasitic patterns").
   Example is pattern: `1б2ве`. Consider word `любвѐ` that should be hyphenated as `люб-вѐ`. When last character is expanded to its NFD
   (decomposed) form, pattern activates and kills valid hyphenation. Removal of this pattern does not affect hyphenation
   of any other dictionary word. We have total of 6 such parasites, listed in `parasitic_patterns.txt`.
   
   ```
   make hyph-cu.tex
   ```

## Generating syllable patterns

```bash
./train.sh > train.log
```

Input here is a hyphenation dictionary `words.txt`. Output is a file `raw_patterns.txt` and `err_raw_patterns.txt` 
containing raw syllable patterns and raw syllable exceptions.

Training parameters were chosen manually after several trial-and-error sessions with the objective to achieve best
possible generalization performance.

For pattern generation we used [pypatgen](https://pypi.python.org/pypi/pypatgen) tool, version 0.2.9. 

Training process is detailed in a [separate document](TRAINING.md).

File `err_raw_patterns.txt` that lists all syllable exceptions in the form
of a full-word pattern. It is used in the next step to make rules more general and more compact.


## Add "long" patterns from exceptions

In the exception list one can often see many variants of a same-root word. It makes sense to make a "long" prefix
pattern to cover this offending root and all its word forms. For example,
```
бо-лѣ́-зней
бо-лѣ́-знемъ
бо-лѣ́-знен-нѡ
бо-лѣ́-знен-ны-ѧ
бо-лѣ́-зни
```
It is much more efficient to replace all these exceptions with a single pattern:
```
.болѣ́7зн
```
The upside is that other forms with the same root will now have correct hyphenation in the root part, even though they were not provided in the dictionary.

Generally speaking, hyphenation of suffixes is more reliable than hyphenation of roots. The reason is that suffix hyphenation
is learned from all words in the dictionary, while root hyphenation - only from words containing this root.

Note that the pattern generation step failed to build this "long" pattern because we limit the pattern length (for better generalization).

To assist in making such "long" prefix patterns, `pypatgen` can generate an error report in the form of suggested full-word
patterns (use option `-p` of the `pypatgen`'s `test` command).

Result of this (manual) work is file `root_patterns.txt` with "long" patterns.


### Adding special rules for combining symbols and digraphs

1. Do not split digraph `LOWERCASE UK` with a hyphen: `U+1C82` `U+0443`
    Also do not split the variant form `U+043E` `U+0443`.

2. Do not allow a hyphen before the following symbols (combiners<sup>[1]</sup>):
   * combining grave: `U+0300` (auto)
   * combining acute: `U+0301` (auto)
   * combining inverted breve: `U+0311` (auto)
   * combining Cyrillic psili pneumata: `U+0486`
   * combining breve: `U+0306`
   * combining vertical tilde: `U+033E`
   * combining paerok: `U+A67D`
   * combining kavyka: `U+A67C`
   * combining dot above: `U+0307`
   * combining diaeresis: `U+0308`
   * combining double grave: `U+030F`
   * combining Cyrillic titlo: `U+0483` (auto)
   * combining pokrytie: `U+0487` (auto)
   * combining Cyrillic letter A: `U+2DF6`
   * combining Cyrillic letter Be: `U+2DE0`
   * combining Cyrillic letter Ve: `U+2DE1` (auto)
   * combining Cyrillic letter Ge: `U+2DE2` (auto)
   * combining Cyrillic letter De: `U+2DE3` (auto)
   * combining Cyrillic letter Ie: `U+2DF7` 
   * combining Cyrillic letter Zhe: `U+2DE4` (auto)
   * combining Cyrillic letter Ze: `U+2DE5` (auto)
   * combining Cyrillic letter I: `U+A675`
   * combining Cyrillic letter Ka: `U+2DE6` (auto)
   * combining Cyrillic letter El: `U+2DE7` (auto)
   * combining Cyrillic letter Em: `U+2DE8` (auto)
   * combining Cyrillic letter En: `U+2DE9` (auto)
   * combining Cyrillic letter O: `U+2DEA`
   * combining Cyrillic letter Pe: `U+2DEB` (auto)
   * combining Cyrillic letter Er: `U+2DEC` (auto)
   * combining Cyrillic letter Es: `U+2DED` (auto)
   * combining Cyrillic letter Te: `U+2DEE`
   * combining Cyrillic letter Monograph Uk: `U+2DF9`
   * combining Cyrillic letter Ef: `U+A69E`
   * combining Cyrillic letter Kha: `U+2DEF` (auto)
   * combining Cyrillic letter Tse: `U+2DF0`
   * combining Cyrillic letter Che: `U+2DF1` (auto)
   * combining Cyrillic letter Sha: `U+2DF2`
   * combining Cyrillic letter Shcha: `U+2DF3`
   * combining Cyrillic letter Yat: `U+2DFA`
   * combining Cyrillic letter Yu: `U+2DFB`
   * combining Cyrillic letter Iotified A: `U+2DFC`
   * combining Cyrillic letter Little Yus: `U+2DFD`
   * combining Cyrillic letter Fita: `U+2DF4`
   * combining Cyrillic letter Es-Te: `U+2DF5` (Note: Unicode discourages use of this character)

Note that other combining letters do not occur in Poluustav or Synodal Slavonic. 
See [UTN 41](http://www.unicode.org/notes/tn41/) for details.

3. Do not hyphenate before:
   * yerok `U+2E2F`
   * yer (ъ) `U+044A`
   * tall yer `U+1C86`
   * soft sign `U+044C`

4. Do not hyphenate before or after these symbols:
   * paerok `U+A67F`
   * kavyka `U+A67E`
   * combining titlo left half: `U+FE2E`
   * combining titlo right half: `U+FE2F`
   * combining conjoining macron: `U+FE26`

In the hand-crafted rules above, mark "(auto)" denotes patterns that were found automatically during step 1.

Result of this work is file `combiner_patterns.txt`. Note that for convenience this file is actually generated programmatically, with
the help of the utility `make_pats.py`.

## Building hyphenation patterns from syllable patterns

To make hyphenation patterns we need to inhibit hyphenation after a leading single-letter syllable and before a trailing single-letter syllable.

To do this we programmatically generate the file `single_patterns.txt`, using the utility `make_pats.py`. These inhibiting patterns
suppress unwanted hyphens, and make a special exception for those few cases when hyphenation after a single letter at the beginning
of a word is allowed.

We run the `build.sh` script to build syllable and hyphenation patterns and to generate the hyphenation TeX file:

```bash
./build.sh > build.log
```
Result is `cu-hyp.tex` and `err_patterns.txt`. The latter lists hyphenation exceptions and is just a different representation of
words within the `\hyphenation` clause in the `cu-hyp.tex`.

## Expanding patterns and exceptions

Input here is `cu-hyp.tex` and the output is `cu-hyph-expanded.tex`.

The hyphenation dictionary contains only the following characters that have different NFD forms:

```python
TABLE = [
    ('\u0400', ['\u0415\u0300']),  # E grave
    ('\u0401', ['\u0415\u0308']),  # IO
    ('\u0403', ['\u0413\u0301']),  # GJE
    ('\u0407', ['\u0406\u0308']),  # YI
    ('\u040c', ['\u041a\u0301']),  # KJE
    ('\u040d', ['\u0418\u0300']),  # I grave
    ('\u040e', ['\u0423\u0306']),  # SHORT U
    ('\u0419', ['\u0418\u0306']),  # SHORT I
    ('\u0439', ['\u0438\u0306']),  # short i
    ('\u0450', ['\u0435\u0300']),  # e grave
    ('\u0451', ['\u0435\u0308']),  # io
    ('\u0453', ['\u0433\u0301']),  # ghe
    ('\u0457', ['\u0456\u0308']),  # yi
    ('\u045c', ['\u043a\u0301']),  # kje
    ('\u045d', ['\u0438\u0300']),  # i grave
    ('\u045e', ['\u0443\u0306']),  # short u
    ('\u0476', ['\u0474\u030f']),  # IZHITSA with double grave
    ('\u0477', ['\u0475\u030f']),  # izhitsa with double grave
    ('\u0479', ['\u1c82\u0443']),  # uk
    ('\u047d', ['\ua64d\u0486\u0311']), # broad omega with veliky apostrof
]
```
and the following recursive function was used to expand each pattern and each exceptional word:

```python
_EXPLODE_MAP = dict(TABLE)
_EXPLODE_REX = re.compile('|'.join(re.escape(x) for x in _EXPLODE_MAP.keys()))

def explode_nfd(string):
    '''
    Takes string and generates all possible equivalent representations by
    substituting each expandable character with all possible NFD expansions.
    '''
    
    string = nfc(string)
    mtc = _EXPLODE_REX.search(string)
    if mtc is None:
        yield string
        return
    
    prefix     = string[:mtc.start()]
    explodable = mtc.group()
    rest       = string[mtc.end():]

    for suffix in explode_nfd(rest):
        yield prefix + explodable + suffix
        
        for expansion in _EXPLODE_MAP[explodable]:
            yield prefix + expansion + suffix
```

[1]: https://cloud.githubusercontent.com/assets/569458/13713500/42d607e2-e797-11e5-9632-10e8b5f6ada2.png
