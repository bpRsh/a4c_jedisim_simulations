#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
# Author    : Bhishan Poudel
# Date      : Jul 20, 2016


# Imports
import os

# output dir
lens = 'physics_settings/lens.txt'
h,t = os.path.split(lens)
if not os.path.isdir(h):
    os.makedirs(h)

# create lens.txt
if not os.path.isfile(lens):
    print('Creating: ', lens)
    with open(lens,'w') as fout:
        line = '6144 6144 1 1000.000000 4.000000' + '\n'
        fout.write(line)



# create psf.txt
psf = 'physics_settings/psf.txt'
if not os.path.isfile(psf):
    print('Creating: ', psf)
    with open(psf,'w') as fout:
        for i in range(21):
            line = 'psf/psf' + str(i) + '.fits' + '\n'
            fout.write(line)
