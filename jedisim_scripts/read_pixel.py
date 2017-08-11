#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Sep 15, 2016
# Last update :

# Inputs      : colors/f606w_gal*.fits
#               colors/f814w_gal*.fits
#
# Outputs     :

# Info:
# 1. This program is for testing.
#
# Estimated time:  24 sec


# Imports
from astropy.io import fits
import numpy as np
import subprocess
import time

# start time
start_time = time.time()



# get data shape from first input file
infile1 = 'colors/f606w_gal0.fits'
infile2 = 'colors/f814w_gal0.fits'

infile3 = 'combination_out/combination_0.fits'
infile4 = 'combination_out2/combination_0.fits'

data1   = fits.getdata(infile1)
data2   = fits.getdata(infile2)

data3   = fits.getdata(infile3)
data4   = fits.getdata(infile4)

a = data1[300][300] # 0.1517767608165741
b = data2[300][300] # 0.21443361043930054

c = data3[300][300] # 0.15804244577884674
d = data4[300][300] # 0.2081679254770279


# ds9 f606_0 300by300 image = 0.106897
# ds9 f814_0 300by300 image = 0.182894
# ds9 combination_0.fits    = 0.193584

# test the values
print('{} {} {}'.format('f606 300 300 = ',a, ''))
print('{} {} {}'.format('f814 300 300 = ',b, ''))
print('{} {} {}'.format('comb c 300 300 = ',c, ''))
print('{} {} {}'.format('comb python 300 300 = ',d, ''))
print('{} {} {}'.format('comb ds9 300 300 = ','0.193584', ''))


# print the time taken
end_time = time.time()
seconds = end_time - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)
print("\nTime taken ==> {:2.0f} days, {:2.0f} hours,\
{:2.0f} minutes, {:f} seconds.".format( d, h, m, s))
