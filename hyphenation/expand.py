#!/usr/bin/env python

from __future__ import unicode_literals
from __future__ import print_function
import argparse
import codecs
import re
import unicodedata


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

_EXPLODE_MAP = dict(TABLE)
_EXPLODE_REX = re.compile('|'.join(re.escape(x) for x in _EXPLODE_MAP.keys()))


def nfc(string):
    ''' NFC-style normalization. Added upcoming Unicode 9.0 "uk" decomposition.'''
    string = unicodedata.normalize('NFC', string)
    string = re.sub('\u1c82\u0443', '\u0479', string)        # uk
    string = re.sub('\ua64d\u0486\u0311', '\u047d', string)  # broad omega with veliky apostrof

    return string

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


def main(args):
    
    with codecs.open(args.input, 'r', 'utf-8') as f:
        with codecs.open(args.output, 'w', 'utf-8') as out:
            
            for line in f:
                for linex in explode_nfd(line):
                    out.write(linex)
    
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Expands hyphenations by generating all combinations of canonically equivalent Unicode representations for a symbol.')
    parser.add_argument('input', help='Input file name')
    parser.add_argument('output', help='Output file name')

    args = parser.parse_args()
    parser.exit(main(args))
