#!/usr/bin/env python

from __future__ import unicode_literals
from __future__ import print_function

import codecs
import argparse

CU_OT = '\u047f'
CU_UK = '\u0479'

CU_UK_NFD = '\u1c82\u0443'

CU_COMBINERS = [
    '\u0300',
    '\u0301',
    '\u0311',
    '\u0486',
    '\u0485',
    '\u0306',
    '\u033e',
    '\ua67d',
    '\ua67c',
    '\u0307',
    '\u0308',
    '\u030f',
    '\u030b',
    '\u1dc0',
    '\u1dc1',
    '\u0302',
    '\u0484',
    '\u0313',
    '\u0314',
    '\u0358',
    '\u1df6',
    '\u1df7',
    '\u1df8',
    '\u1df9',
    '\u0483',
    '\ua66f',
    '\u0487',
    '\u0305',
    '\u033f',
    '\u2df6',
    '\u2de0',
    '\u2de1',
    '\u2de2',
    '\u2de3',
    '\u2df7',
    '\ua674',
    '\u2de4',
    '\u2de5',
    '\ua675',
    '\ua676',
    '\u2df8',
    '\u2de6',
    '\u2de7',
    '\u2de8',
    '\u2de9',
    '\u2dea',
    '\u2deb',
    '\u2dec',
    '\u2ded',
    '\u2dee',
    '\u2df9',
    '\ua677',
    '\ua69e',
    '\u2def',
    '\ua67b',
    '\u2df0',
    '\u2df1',
    '\u2df2',
    '\u2df3',
    '\ua678',
    '\ua67a',
    '\ua679',
    '\u2dfa',
    '\u2dfb',
    '\u2dfc',
    '\ua69f',
    '\u2dfd',
    '\u2dfe',
    '\u2dff',
    '\u2df4',
    '\u2df5',
]
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
    '\u0430',
    '\u0435',
    '\u0438',
    '\u0439',
    '\u043e',
    '\u0443',
    '\u044b',
    '\u044d',
    '\u044e',
    '\u044f',
    '\u0450',
    '\u0454',
    '\u0456',
    '\u0457',
    '\u0458',
    '\u0461',
    '\u0463',
    '\u0465',
    '\u0467',
    '\u0469',
    '\u046b',
    '\u046d',
    '\u0475',
    '\u0477',
    '\u047b',
    '\u047d',
    '\u047f',
    '\ua657',
    '\ua659',
    '\ua65b',
    '\ua65f',
    '\ua65d',
]

CU_BREATHING = '\u0486'
CU_BREATHING_HARD = '\u0485'


def main_combining(args):

    inh = str(args.inhibiting_level)

    with codecs.open(args.output, 'w', 'utf-8') as f:
        f.write('% Combiners and related special patterns\n')
        f.write(inh.join(CU_UK_NFD)
                + '  % Do not split digraph `LOWERCASE UK` with a hyphen: `U+1C82` `U+0443`\n')
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
            for y in CU_COMBINERS:
                f.write('.' + x + y + inh + '\n')
                f.write('.' + x + CU_BREATHING + y + inh +'\n')
                f.write('.' + x + CU_BREATHING_HARD + y + inh +'\n')
        f.write('%\n')
        f.write('% Forbid hyphenation before a single letter (with all possible and impossible combiners!)\n')
        for x in CU_VOWELS:
            f.write(inh + x + '.\n')
            for y in CU_COMBINERS:
                f.write(inh + x + y + '.\n')
                f.write(inh + x + CU_BREATHING + y +'.\n')
                f.write(inh + x + CU_BREATHING_HARD + y +'.\n')
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
