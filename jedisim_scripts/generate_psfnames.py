#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : Bhishan Poudel
# Date      : Jul 26, 2016

# Imports
from __future__ import print_function 

num_outfiles = 20
outfile = "physics_settings/psf.txt"
with open (outfile, 'w') as fout:
    for i in range(num_outfiles):
        print('psf/psf{:-d}.fits'.format(i),file=fout)
    

print('{} {} {}'.format('output file : ',outfile, ''))
