#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 12, 2016
# Last update :
#
# Inputs      : 21 input psf from unnormalized psf directory
# Outputs     : 21 output psf inside normalized psf directory
#
# Info:
# 1. This program will get the sum of all the pixels in a fitsfile.
#
# Estimated time : 1 minute 22 seconds
#

# Imports
from astropy.io import fits
import numpy as np
import time


# ==============================================================================
# replace_outdir
# ==============================================================================
def replace_outdir(outdir):
    """Replace ouptut directory."""
    # imports
    import shutil
    import os

    if os.path.exists(outdir):
        print('Replacing folder: ', outdir)
        shutil.rmtree(outdir)
        os.makedirs(outdir)
    else:
        print('Making new folder: ', outdir)
        os.makedirs(outdir)


def normalize_psf(indir, outdir):
    """Normalize all the psf to total sum = 1."""
    # indir  = 'phosim_output_unzipped'
    # outdir = 'phosim_normalized_psf'

    for i in range(21):

        infile = indir + '/psf{:d}.fits'.format(i)
        data = fits.getdata(infile)
        shape = data.shape

        rows = data.shape[0]
        total = 0.0
        for j in range(rows):
            total += sum(data[j])

        # update the data after getting total of all rows
        for k in range(rows):
            data[k] /= total

        # output data
        outfile = outdir + '/psf' + str(i) + '.fits'
        hdu = fits.PrimaryHDU()
        hdu.data = data
        hdu.writeto(outfile, clobber=True)

        # output info
        print('\ninput file  : ', infile)
        print('{} {} {}'.format('output file : ', outfile, ''))


if __name__ == '__main__':

    # beginning time
    program_begin_time = time.time()
    begin_ctime = time.ctime()

    # replace outdir
    outdir = 'normalized_psf'
    replace_outdir(outdir)

    # normalize psf
    indir = 'psf'
    outdir = 'normalized_psf'
    normalize_psf(indir, outdir)

    # print the time taken
    program_end_time = time.time()
    end_ctime = time.ctime()
    seconds = program_end_time - program_begin_time
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print('\nBegin time: ', begin_ctime)
    print('End   time: ', end_ctime, '\n')
    print("Time taken: {0:.0f} days, {1:.0f} hours, \
          {2:.0f} minutes, {3:f} seconds.".format(d, h, m, s))
