#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import codecs
import argparse

CU_OT = '\u047f'
CU_UK = '\u0479'

CU_UK_NFD = '\u1c82\u0443'
CU_UK_NFD2 = '\u043e\u0443'

CU_ACCENTS_1 = [  # Aleksandr put only those for the start of the word patterns
    '\u0300',
    '\u0301',
    '\u0311',
    '\u0308'
]

CU_ACCENTS_2 = [
    unichr(x) for x in range(ord('\u2de0'), ord('\u2dff')+1)
] + [
    unichr(x) for x in range(ord('\ua674'), ord('\ua67d')+1)
]

CU_POKRYTIE = 'u0487'

CU_COMBINERS = CU_ACCENTS_1 + [
    '\u0486',
    '\u0306',
    '\u033e',
    '\ua67d',
    '\ua67c',
    '\u0307',
    '\u030f',
    '\u0483',
    '\u0487',
] + CU_ACCENTS_2

CU_YEROK     = '\u2e2f'
CU_YER       = '\u044a'
CU_TALL_YER  = '\u1c86'
CU_SOFT_SIGN = '\u044c'

CU_PAEROK = '\ua67f'
CU_KAVYKA = '\ua67e'
CU_COMB_TITLO_LEFT = '\ufe2e'
CU_COMB_TITLO_RIGHT = '\ufe2f'
CU_COMB_CONJ_MACRON = '\ufe26'

CU_VOWELS = [
    '\u0430',  # а
    '\u0435',  # е
    '\u0454',  # є
    '\u0438',  # и
    '\u0439',  # й
    '\u0456',  # i
    '\u043e',  # о
    '\u1c82',  # sharp o
    '\u047b',  # ѻ
    '\u0461',  # ѡ
    '\u047d',  # ѽ
    '\u047f',  # ѽ
    '\ua64d',  # ꙍ
    '\u044b',  # ы
    '\u044d',  # э
    '\u0463',  # ѣ
    '\u044e',  # ю
    '\u0467',  # ѧ
    '\ua657',  # ꙗ
    '\u0475',  # ѵ
    '\u0443',  # у
    '\ua64b',  # ꙋ
    '\u0479',  # ѹ
]

CU_BREATHING = '\u0486'
CU_BREATHING_HARD = '\u0485'

def main_combining(args):

    inh = str(args.inhibiting_level)

    with codecs.open(args.output, 'w', 'utf-8') as f:
        f.write('% Combiners and related special patterns\n')

        f.write(inh.join(CU_UK_NFD)
                + '  % Do not split digraph `LOWERCASE UK` with a hyphen: `U+1C82` `U+0443`\n')
        f.write(inh.join(CU_UK_NFD2)
                + '  % Do not split this gorm of digraph `LOWERCASE UK` with a hyphen: `U+043e` `U+0443`\n')
        f.write('% combiners: never split before any combining symbol\n')

        for x in CU_COMBINERS:
            f.write(inh + x + '\n')
        f.write('%\n')
        
        for x in (CU_YER, CU_YEROK, CU_TALL_YER, CU_SOFT_SIGN):
            f.write(inh + x + '\n')
        
        f.write('% do not hyphenate before nor after those:\n')
        for x in (CU_PAEROK, CU_KAVYKA, CU_COMB_TITLO_LEFT, CU_COMB_TITLO_RIGHT, CU_COMB_CONJ_MACRON):
            f.write(inh + x + inh + '\n')
        f.write('% end combining and special patterns\n')


def main_singles(args):

    inh = str(args.inhibiting_level)

    with codecs.open(args.output, 'w', 'utf-8') as f:
        f.write('% Forbid hyphenation after a single letter\n')
        for x in CU_VOWELS:
            if x in (CU_UK, CU_OT):
                continue
            f.write('.' + x + inh + '\n')
            for y in CU_ACCENTS_1:
                f.write('.' + x + y + inh + '\n')
                f.write('.' + x + CU_BREATHING + y + inh +'\n')
            for y in CU_ACCENTS_2:
                f.write('.' + x + y + inh + '.\n')
                f.write('.' + x + y + CU_POKRYTIE + inh + '.\n')
        f.write('%\n')

        f.write('% Forbid hyphenation before a single letter (with all possible and impossible combiners!)\n')
        for x in CU_VOWELS:
            f.write(inh + x + '.\n')
            for y in CU_ACCENTS_1:
                f.write('.' + x + y + inh + '\n')
                f.write('.' + x + CU_BREATHING + y + inh +'\n')
            for y in CU_ACCENTS_2:
                f.write(inh + x + y + '.\n')
                f.write(inh + x + y + CU_POKRYTIE + '.\n')
        f.write('% end single-letter rules\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates combining hyphenation inhibiting patterns fo Church Slavonic.')
    parser.add_argument('type', help='Type of patterns to generate - one of ["combining", "singles"]')
    parser.add_argument('output', help='Output file name')
    parser.add_argument('-i', '--inhibiting_level', type=int, default=8, help='Output file name')

    args = parser.parse_args()
    
    
    if args.inhibiting_level <=0 or args.inhibiting_level > 8:
        raise ValueError('--inhibiting_level not in range. Expect to be between 2 and 8.')
    if args.inhibiting_level % 2 == 1:
        raise ValueError('--inhibiting_level must be an even number')
    
    if args.type == 'combining':
        parser.exit(main_combining(args))
    elif args.type == 'singles':
        parser.exit(main_singles(args))
    else:
        parser.error('Unrecognized pattern type "%s". Expect one of ["combining", "singles"]' % args.type)
