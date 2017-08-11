#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 20, 2016
# Last update :
#

# Imports
from __future__ import print_function






##==============================================================================
## catalog.txt :  angle --> angle+90     out0 --> 90_out0   look at the bottom
##==============================================================================

# rotate the angle of catalog.txt by 90 degree
infile  = 'jedisim_out/out0/trial0_catalog.txt'
outfile = 'jedisim_out/90_out0/90_trial0_catalog.txt'

with open (infile,'r') as fin, open(outfile, 'w') as fout:
    for old_line in fin:

        l = old_line.split("\t")

        angle = float(l[3])
        angle2 = angle + 90.0

        if angle2>= 360:
            angle2 = angle2 - 360

        l[3] = str(angle2)
        #print('{} {} {}'.format('angle before: ',angle, ''))
        #print('{} {} {}'.format('angle after: ',angle2, ''))
        l[-1]= l[-1].replace('jedisim_out/out0/distorted_0','jedisim_out/90_out0/distorted_0')

        l[-2]= l[-2].replace('jedisim_out/out0/stamp_0','jedisim_out/90_out0/stamp_0')
        line = "\t".join(l)
        fout.write(line)
    print('Creating: ', outfile)





##==============================================================================
## convolvedlist.txt   out0 --> 90_out0
##==============================================================================
# create new convolved list from old list
# old     : jedisim_out/out0/trial0_convolvedlist.txt
# contents: jedisim_out/out0/convolved/convolved_band_0.fits_upto_5.fits
# needed  : jedisim_out/90_out0/convolved/convolved_band_0.fits

infile  = 'jedisim_out/out0/trial0_convolvedlist.txt'
outfile = 'jedisim_out/90_out0/90_trial0_convolvedlist.txt'
with open(infile,'r') as fin, open(outfile,'w') as fout:
    for old_line in fin:
        line = old_line.replace('out0','90_out0')
        fout.write(line)
    print('Creating: ' , outfile)







##==============================================================================
## distortedlist.txt  out0 --> 90_out0
##==============================================================================
# create new distorted list from old list
# old      : jedisim_out/out0/trial0_distortedlist.txt
# contents : jedisim_out/out0/distorted_0/distorted_0.fits_upto_1000.fits
# needed   : jedisim_out/90_out0/distorted_0/distorted_0.fits_upto_1000.fits
infile  = 'jedisim_out/out0/trial0_distortedlist.txt'
outfile = 'jedisim_out/90_out0/90_trial0_distortedlist.txt'
with open(infile,'r') as fin, open(outfile,'w') as fout:

    for old_line in fin:
        line = old_line.replace('out0','90_out0')
        fout.write(line)
    print('Creating: ', outfile)











##==============================================================================
# jedisim_out/out0/trial0_catalog.txt
##==============================================================================
# jedisim_out/color_out/color_out0/blue_red_62.fits  3183.222412 9061.648438 185.040207  1.500000    0.030000
# input_for_jeditransform                            x           y           angle        redshift   pixscale

# 23.689899   0.218280    27.730000   0.090300
# old_mag     old_rad     new_mag     new_rad

# jedisim_out/color_out/color_out0/blue_red_62.fits 3183.222412 9061.648438 275.040207  1.500000    0.030000
# 23.689899   0.218280    27.730000   0.090300
# jedisim_out/90_out0/stamp_0/stamp_0.fits.gz jedisim_out/90_out0/distorted_0/distorted_0.fits


##==============================================================================
# jedisim_out/90_out0/90_trial0_catalog.txt: angle added 90 degree and out --> 90_out
##==============================================================================
# jedisim_out/color_out/color_out0/blue_red_62.fits 3183.222412 9061.648438 275.040207  1.500000    0.030000
# 23.689899 0.218280    27.730000   0.090300
# jedisim_out/90_out0/stamp_0/stamp_0.fits.gz   jedisim_out/90_out0/distorted_0/distorted_0.fits



