#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author    : Bhishan Poudel
# Date      : Jul 26, 2016

# Imports
from __future__ import print_function

num_outfiles = 21
for count in range(1):

    outfile   = "physics_settings/rescaled_convolved_lsst_out{:d}.txt".format(count)
    outfile90 = "physics_settings/rescaled_convolved_lsst_90_out{:d}.txt".format(count)
    with open (outfile, 'w') as f, open(outfile90, 'w') as f90:

        print('Creating: ', outfile)
        print('Creating: ', outfile90)
        for i in range(num_outfiles):
            print('jedisim_out/rescaled_convolved_lsst_out{:d}/rescaled_convolved_lsst_{:-d}.fits'.format(count,i),file=f)
            print('jedisim_out/rescaled_convolved_lsst_out{:d}/90_rescaled_convolved_lsst_{:-d}.fits'.format(count,i),file=f90)


