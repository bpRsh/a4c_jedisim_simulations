#!/usr/bin/env python3
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Nov 21, 2016
# Last update :
# Est time    : 3 sec

# Imports
from __future__ import division, unicode_literals, print_function
import subprocess
import os
import shutil
import time
from astropy.io import fits


def create_null_fits(infits, outfits):
    """Create null fitsfiles.

    Arguments:
    infits: input fitsfile
    outfits: path name for output fitsfile

    Depends: disk, an empty folder
    """
    # read data and header from input fitsfiles

    dat, hdr = fits.getdata(infits, header=True)
    try:
        del hdr['BYTEORDR']
    except:
        pass

    hdr['BYTEORDR'] = 'BIG_ENDIAN'

    # data for output fitsfile
    dat_out = dat * 0.0
    fits.writeto(outfits, dat_out, hdr, clobber=True)


def main():
    """Main program."""
    # input/output fitsfiles
    infits = 'colors/f606w_gal0.fits'
    nullfits = 'null.fits'
    create_null_fits(infits, nullfits)

    for i in list(range(101)):
        shutil.copyfile(nullfits, "disk/f606w_disk{:d}.fits".format(i))
        shutil.copyfile(nullfits, "disk/f814w_disk{:d}.fits".format(i))

    # after done copying same file again and again, delete the file
    if os.path.isfile('null.fits'):
        os.remove('null.fits')

if __name__ == '__main__':

    #  beginning time
    program_begin_time = time.time()
    begin_ctime = time.ctime()

    # run main program
    main()

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
