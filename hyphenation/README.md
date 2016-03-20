# Creating hyphenation patterns for Church Slavonic

We create TeX hyphenation patterns in the following stages

1. Use the hyphenation dictionary to automatically generate patterns. 
   Since dictionary uses [Normal Form C](http://unicode.org/reports/tr15/), all patterns will also be in this form.

2. Analyze errors that patterns make on the hyphenation dictionary and add (long) patterns that cover offending stems. This
   essentially allows one to move some errors out of the exception list into patterns, hoping that the new pattern will
   cover all word forms (not just forms seen within the training dictionary).

3. Add special patterns that ensure that no hyphenation happens before a combining character. Since Church Slavonic
   uses a rich set of diacritical marks, we do not rely on step 1 to find all of these places, and just add these rules 
   explicitly

4. Expand patterns and exception list by replacing each character with its Normal Form D. Note that for robustness
   we create all combinations of D and C forms for every character that has these different forms. This is different
   from just converting each pattern and exception to Normal Form D.

## Generating patterns

```bash
./train.sh > train.log
```

Input here is a hyphenation dictionary `words.txt`. Output is a file `cu-hyp-patterns.txt` and `cu-hyp-excpetions.txt` 
containing hyphenation patterns and hyphenation exceptions.

Training parameters were chosen manually after several trial-and-error sessions with the objective to achieve best
possible generalization performance.

For pattern generation we used [pypatgen](https://pypi.python.org/pypi/pypatgen) tool, version 0.2.9. 

Training process is detailed in a [separate document](TRAINING.md).

Auxiliary output file is `err_patterns.txt` that lists all hyphenation exceptions in the form
of a full-word pattern. It is used in the next step to make hyphenation rules more general and more compact.


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
The upside is that other forms of the same root will now have correct hyphenation in the root part, even though they were not provided in the dictionary.

Generally speaking, hyphenation of suffixes is more reliable than hyphenation of roots. The reason is that suffix hyphenation
is learned from all words in the dictionary, while root hyphenation - only from words containing this root.

Note that the pattern generation step failed to build this "long" pattern because we limit the pattern length (for better generalization).

To assist in making such "long" prefix patterns, `pypatgen` can generate an error report in the form of suggested full-word
patterns (use option `-p` of the `pypatgen`'s `test` command).

Result of this (manual) work is file `root_patterns.txt` with "long" patterns.


### Adding special rules for combining symbols and digraphs

1. Do not split digraph `LOWERCASE UK` with a hyphen: `U+1C82` `U+0443`
    Also do not split the variant form `U+043E` `U+0443`.

2. Do not allow a hyphen before the following symbols (combiners[1]):
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

Result of this work is file `combiner_patterns.txt`. Note that for the convenience this file is actually generated programmatically, with
the help of utility `make_pat.py`.

We then run the script to build the hyphenation TeX file:

```bash
./build.sh > build.log
```
Result is `cu-hyp.tex`.

## Expanding patterns and exceptions

Input here is `cu-hyp.tex` and the output is `cu-hyph-expanded.tex`.

The hyphenation dictionary contains only the following characters that have different NFD form:

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
