#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : Bhishan Poudel
# Date      : Jul 26, 2016

# Imports
from __future__ import print_function

num_galaxies = 101

# for bulge part
outfile = "physics_settings/bulge.txt"
with open(outfile, 'w') as fout:
    for i in range(101):
        print(
            'simdatabase/bulge/f606w_bulge{:-d}.fits    simdatabase/bulge/f814w_bulge{:-d}.fits       simdatabase/bulge_blue_red/out{:-d}.fits'.format(i, i, i), file=fout)


print('{} {} {}'.format('output file : ', outfile, ''))

# for disk part
outfile = "physics_settings/disk.txt"
with open(outfile, 'w') as fout:
    for i in range(101):
        print(
            'simdatabase/disk/f606w_disk{:-d}.fits    simdatabase/disk/f814w_disk{:-d}.fits       simdatabase/disk_blue_red/out{:-d}.fits'.format(i, i, i), file=fout)


print('{} {} {}'.format('output file : ', outfile, ''))
