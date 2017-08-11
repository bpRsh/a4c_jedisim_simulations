#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Imports
from astropy.io import fits
import numpy as np
import subprocess
import time

# start time
start_time = time.time()

##==============================================================================
## replace_outdir
##==============================================================================
def replace_outdir(outdir):

    # imports
    import shutil,os

    if os.path.exists(outdir):
        print('Replacing folder: ', outdir)
        shutil.rmtree(outdir)
        os.makedirs(outdir)
    else:
        print('Making new folder: ', outdir)
        os.makedirs(outdir)




outdir = 'difference_out'
replace_outdir(outdir)


nfiles = 100
for i in range(0,100):
    # get data shape from first input file
    infile1 = 'colors/f606w_gal{:d}.fits'.format(i)
    data1   = fits.getdata(infile1)
    shape1   = data1.shape


    # get data shape from first second file
    infile2 = 'colors/f814w_gal{:d}.fits'.format(i)
    data2   = fits.getdata(infile2)
    shape2  = data2.shape




    # output data
    outfile = outdir + '/diff_{:d}.fits'.format(i)
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
