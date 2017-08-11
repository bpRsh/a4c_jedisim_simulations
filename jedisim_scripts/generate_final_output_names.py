#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : Bhishan Poudel
# Date      : Jul 26, 2016

# Imports
from __future__ import print_function

num_outfiles = 21
outfile1 = "physics_settings/out.txt"
outfile2 = "physics_settings/90_out.txt"
with open(outfile1, 'w') as fout1, open(outfile2, 'w') as fout2:
    for i in range(num_outfiles):
        print('aout/aout{:-d}.fits'.format(i, i, i), file=fout1)
        print('aout/90_aout{:-d}.fits'.format(i, i, i), file=fout2)


print('{} {} {}'.format('output file : ', outfile1, ''))
print('{} {} {}'.format('output file : ', outfile2, ''))
