#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
#
# Author    : Bhishan Poudel
# Date      : Jul 26, 2016

# Imports
from __future__ import print_function

outfile = "physics_settings/rescaled_convolved_lsst_21.txt"
with open (outfile, 'w') as f:
    for i in range(21):
        print('jedisim_out/rescaled_convolved_lsst_21/rescaled_convolved_lsst_{:d}.fits'.format(i),file=f)

