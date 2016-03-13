# Creating hyphenation patterns for Church Slavonic

We create TeX hyphenation patterns in the following stages

1. Use the hyphenation dictionary to automatically generate patterns. 
   Since dictionary uses [Normal Form C](http://unicode.org/reports/tr15/), all patterns will also be in this form.

2. Analyze errors that patterns make on the hyphenation dictionary and add (long) patterns that cover offending stems. This
   essentially allows one to move some errors out of exception list into a patterns, hoping that new pattern will
   cover all word forms (not just forms seen within the training dictionary).

3. Expand patterns and exception list by replacing each character with its Normal Form D. Note that for robustness
   we create all combinations of D and C forms for every character that has these different forms. This is different
   from just converting each pattern and exception to Normal form D.

4. Add special patterns that ensure that no hyphenation happens before a combining character. Since Church Slavonic
   uses rich set of diacritical marks, we do not rely on step 1 finding all this places, and just add these rules 
   explicitly

## Generating patterns

Input here is a hyphenation dictionary `words.txt`. Output is a file `cu-hyph.tex` containing hyphenation patterns and
hyphenation exceptions.

Training parameters were chosen manually after several trial-and-error sessions with the objective to achieve best
possible generalization performance.

We used [pypatgen](tool for pattern generation). 

Training process is detailed in the [following document](TRAINING.md).

Auxilliary output file is `err_patterns.txt` that lists all hyphenation exceptions in the form
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
The upside is that other forms of the same root will have correct hyphenation in the root part.

Generally speaking, hyphenation of suffixes is more reliable than hyphenation of roots. Reason is that suffix hyphenation
is learned from all words in the dictionary, whicle root hyphenation - only from words containing this root.

Note that pattern generation step failed to build this "long" pattern because we limit the pattern length (for better generalization).

To assist in making such "long" prefix patterns, `pypatgen` can generate error report in the form of suggested full-word
patterns (use option `-p` of the `pypatgen`'s `test` command).

Result of this work is fule `cu-hyp2.tex`

## Expanding patterns and exceptions

Input here is `cu-hyp2.tex` and the output is `cu-hyph-expanded.tex`.

The hyphenation dictionary contains only following characters that have different NFD form:

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

### Adding special rules for combining symbols and digraphs

1. Do not split digraph `LOWERCASE UK` with a hyphen: `U+1C82` `U+0443`

2. Do not allow hyphen before the following symbols (combiners[1]):
   * combining grave: `U+0300` (auto)
   * combining acute: `U+0301` (auto)
   * combining inverted breve: `U+0311` (auto)
   * combining Cyrillic psili pneumata: `U+0486`
   * combining Cyrillic dasia pneumata: `U+0485`
   * combining breve: `U+0306`
   * combining vertical tilde: `U+033E`
   * combining paerok: `U+A67D`
   * combining kavyka: `U+A67C`
   * combining dot above: `U+0307`
   * combining diaeresis: `U+0308`
   * combining double grave: `U+030F`
   * combining double acute: `U+030B`
   * combining dotted grave: `U+1DC0`
   * combining dotted acute: `U+1DC1`
   * combining circumflex: `U+0302`
   * combining palatalization: `U+0484`
   * combining comma above: `U+0313`
   * combining reversed comma above: `U+0314`
   * combining reversed dot right: `U+0358`
   * combining kavyka above right: `U+1DF6`
   * combining kavyka above left: `U+1DF7`
   * combining dot above left: `U+1DF8`
   * combining wide inverted bridge below: `U+1DF9`
   * combining Cyrillic titlo: `U+0483` (auto)
   * combining vzmet: `U+A66F`
   * combining pokrytie: `U+0487` (auto)
   * combining overline: `U+0305`
   * combining double overline: `U+033F`
   * combining Cyrillic letter A: `U+2DF6`
   * : `U+2DE0`
   * : `U+2DE1` (auto)
   * : `U+2DE2` (auto)
   * : `U+2DE3` (auto)
   * : `U+2DF7` 
   * : `U+A674`
   * : `U+2DE4` (auto)
   * : `U+2DE5` (auto)
   * : `U+A675`
   * : `U+A676`
   * : `U+2DF8`
   * : `U+2DE6` (auto)
   * : `U+2DE7` (auto)
   * : `U+2DE8` (auto)
   * : `U+2DE9` (auto)
   * : `U+2DEA`
   * : `U+2DEB` (auto)
   * : `U+2DEC` (auto)
   * : `U+2DED` (auto)
   * : `U+2DEE`
   * : `U+2DF9`
   * : `U+A677`
   * : `U+A69E`
   * : `U+2DEF` (auto)
   * : `U+A67B`
   * : `U+2DF0`
   * : `U+2DF1` (auto)
   * : `U+2DF2`
   * : `U+2DF3`
   * : `U+A678` (auto)
   * : `U+A67A`
   * : `U+A679`
   * : `U+2DFA`
   * : `U+2DFB`
   * : `U+2DFC`
   * : `U+A69F`
   * : `U+2DFD`
   * : `U+2DFE`
   * : `U+2DFF`
   * : `U+2DF4`
   * : `U+2DF5`
   
3. Do not hyphenate before:
   * yerok `U+2E2F`
   * yer (ъ) `U+044A`
   * tall yer `U+1C86`

4. Do not hyphenate before or after those symbols:
   * paerok `U+A67F`
   * kavyka `U+A67E`
   * combining titlo left half: `U+FE2E`
   * combining titlo right half: `U+FE2F`
   * combining conjoining macron: `U+FE26`

In the hand-crafted rules above mark "(auto)" denotes patterns that were found automatically during step 1.
 
[1]: https://cloud.githubusercontent.com/assets/569458/13713500/42d607e2-e797-11e5-9632-10e8b5f6ada2.png
