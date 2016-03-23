#!/usr/bin/env python

from __future__ import unicode_literals
from __future__ import print_function

import argparse
import unicodedata
import codecs

CU_OT    = '\u047f'
CU_OMEGA = '\u0461'
CU_UK    = '\u0479'

def num_letters(s):
    '''counts letters in a string (ignores combining symbols)'''
    return sum(1 for x in s if not unicodedata.combining(x))

def hyph_from_syls(s):
    '''makes a hyphenation pattern from a syllable pattern for Church Slavonic'''
    parts = s.split('-')
    
    if len(parts) > 1:
        if num_letters(parts[0]) < 2 and parts[0][0] not in (CU_OT, CU_UK, CU_OMEGA):
            # remove hyphen by merging with next syllable
            parts[1] = parts[0] + parts[1]
            parts.pop(0)

    if len(parts) > 1:
        if num_letters(parts[-1]) < 2:
            # remove hyphen by merging with next syllable
            parts[-2] = parts[-2] + parts[-1]
            parts.pop()
    
    return '-'.join(parts)


def main(args):
    
    with codecs.open(args.input, 'r', 'utf-8') as f:
        
        with codecs.open(args.output, 'w', 'utf-8') as out:
            for line in f:
                line = line.strip()
                out.write(hyph_from_syls(line) + '\n')
    return 0

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Converts Church Slavonic syllable dictionary to hyphenation dictionary')
    parser.add_argument('input', help='Name of the input file (a syllable dictionary)')
    parser.add_argument('output', help='Name of the output file (a hyphenation dictionary)')

    args = parser.parse_args()
    
    parser.exit(main(args))
