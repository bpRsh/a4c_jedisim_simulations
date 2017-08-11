#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Imports
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time

# start time
start_time = time.time()


# get data shape from first input file
infile1 = 'combination_out/combination_0.fits'
data1   = fits.getdata(infile1)


# get data shape from first second file
infile2 = 'combination_out2/combination_0.fits'
data2   = fits.getdata(infile2)




# output data
outfile = 'test.fits'
dout = data1 - data2
hdu  = fits.PrimaryHDU()
hdu.data = dout
hdu.writeto(outfile, clobber=True)

#output info
print('{} {} {}'.format('\ninfile1     : ',infile1, ''))
print('{} {} {}'.format('infile2     : ',infile2, ''))
print('{} {} {}'.format('output file : ',outfile, ''))

# print the time taken
end_time = time.time()
seconds = end_time - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)
print("\nTime taken ==> {:2.0f} days, {:2.0f} hours,\
{:2.0f} minutes, {:f} seconds.".format( d, h, m, s))
