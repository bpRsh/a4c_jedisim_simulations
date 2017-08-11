#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
# Author    : Bhishan Poudel
# Date      : Jul 26, 2016
# Updated   : Wed Mar 15, 2017
# Info:
# simdatabase/bulge/f606w_bulge0.fits etc are obtained from galfit

# Imports
import os

num_galaxies = 302

# create color.txt
# jedicolor will scale first two fits files and writes the last one.
# bulge and disk are obtained from two component fitting of galfit.
# The galfit takes in input galaxy provided by collaboraters, and makes
# gets bulge and disk part from each galaxy.
# Not all the galaxies have two components, the one which does not have
# disk part is taken as bulge and disk is null fits of same dimension.
phy = 'physics_settings'
color_out = 'simdatabase/bulge_disk_f8'

# physics_settings
if not os.path.isdir(phy):
    os.makedirs(phy)

# simdatabase/color_output_folder
if not os.path.isdir(color_out):
    os.makedirs(color_out)
    
    
outfile = phy + "/color.txt"

with open(outfile, 'w') as fout:
    for i in range(num_galaxies):
        in1 = '/Users/poudel/jedisim/simdatabase/bulge_f8/f814w_bulge' + str(i) + '.fits'
        in2 = '/Users/poudel/jedisim/simdatabase/disk_f8/f814w_disk'   + str(i) + '.fits'
        out = 'simdatabase/bulge_disk_f8/f8_bulge_disk' + str(i) + '.fits'
        line = '  '.join([in1, in2, out])
        print(line, file=fout)

print('{} {} {}'.format('output file : ', outfile, ''))

# lines of color.txt
# /Users/poudel/jedisim/simdatabase/bulge_f8/f814w_bulge0.fits  /Users/poudel/jedisim/simdatabase/disk_f8/f814w_disk0.fits  simdatabase/bulge_disk_f8/f8_bulge_disk0.fits
