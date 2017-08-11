#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Sep 15, 2016
# Last update :

# Inputs      : colors/f606w_gal*.fits
#               colors/f814w_gal*.fits
#               
# Outputs     : combination/redblue*.fits

# Info:
# 1. This program takes in two input fits files and creates difference of them.
#
# Estimated time:  24 sec               


# Imports
from astropy.io import fits
import numpy as np
import subprocess
import time

# start time
start_time = time.time()

number = 0.1
nfiles = 3
for i in range(0,nfiles):

    # get data shape from first input file
    infile1 = 'colors/diff{:d}.fits'.format(i)
    data1   = fits.getdata(infile1)
    shape1  = data1.shape
    
    
    
    # get data shape from first second file
    infile2 = 'colors/f814w_gal{:d}.fits'.format(i)
    data2   = fits.getdata(infile2)
    shape2  = data2.shape
    
    
    
    
    
    # output data
    outfile = 'combination/combination_{:d}.fits'.format(i)
    dout = data1 * number + data2
    hdu  = fits.PrimaryHDU()
    hdu.data = dout
    hdu.writeto(outfile, clobber=True)


    
    #output info
    print('{} {} {}'.format('\ninfile1     : ',infile1, ''))
    print('{} {} {}'.format('infile2     : ',infile2, ''))
    print('{} {} {}'.format('output file : ',outfile, ''))


    # checking some values
    print('{} {} {}'.format('\ndata1 300 300 = ',data1[300][300], ''))
    print('{} {} {}'.format('data1 300 300 = ',data2[300][300], ''))
    print('{} {} {}'.format('dout 300 300 = ',dout[300][300], ''))

# print the time taken
end_time = time.time()
seconds = end_time - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)
print("\nTime taken ==> {:2.0f} days, {:2.0f} hours,\
{:2.0f} minutes, {:f} seconds.".format( d, h, m, s))
