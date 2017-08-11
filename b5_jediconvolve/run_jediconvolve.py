#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 17, 2016
# Last update : May 08, 2017
#
# Estimated time: 27 minutes for 302 galaxies (12420 stamps)
# Depends     : 1. fitsfile_to_convolve : jedisim_out/out0/trial0_HST.fits
#            2. psf_to_convolve_with : psf/psf0.fits
#               3. output_path_to_write_6_bands: jedisim_out/out0/convolved
#
#
# Output      : 1. convolved_band_0_to_5.fits : 6 convolved bands
#
#
# Jedimaster  : color, jedicatalog, color, jeditransform, jedidistort, jedipaste,
#                      jediconvolve, jedipaste, jedirescale
#
# Info: This program will convolve the HST.fits (i.e. out1/trial0_HST.fits)
#       with the given psf (i.e. psf/psf0.fits) and writes 6 bands of convolved images
#       (i.e. out1/convolved/convolved_band_0_to_5.fits ) 
#       and later jedipaste will writes out out1/trial0_HST_convolved.fits
#
# Imports
import os
import shutil
import subprocess
import sys
import time


def run_process(name, args,):

    '''Usage: run_process("example ", ["python ", 'example.py', 'arg1' ])    '''

    print("\n\n\n","#"*40)
    print("# Description : %s\n# Commands :"%name,end=' ')
    for arg in args:
        print(arg, end=' ')

    print("\n","#"*39,end='\n\n')

    process = subprocess.Popen(args)

    process.communicate()
    if process.returncode != 0:
        print("Error: %s did not terminate correctly. \
              Return code: %i."%(name, process.returncode))
        sys.exit(1)
    else:
        print("\n\n", "#"*39,end='\n')
        print("# Success! : %s "%name)
        print("#"*40,"\n\n\n")

if __name__ == '__main__':

    # beginning time
    program_begin_time = time.time()
    begin_ctime        = time.ctime()

    # replace old outputs
    convolved = 'out1/convolved'
    if os.path.exists(convolved):
        shutil.rmtree(convolved)
        os.makedirs(convolved)
    else:
        os.makedirs(convolved)


    # run program
    # executable nx ny dislist lens  pix  redshift
    run_process("jediconvolve ", ['./jediconvolve', \
                'out1/trial0_HST.fits', \
                'psf/psf0.fits', \
                'out1/convolved/' ])

    # delete pycache folder
    pycache = '__pycache__'
    if os.path.exists(pycache): shutil.rmtree(pycache)


    # print the time taken
    program_end_time = time.time()
    end_ctime        = time.ctime()
    seconds          = program_end_time - program_begin_time
    m, s             = divmod(seconds, 60)
    h, m             = divmod(m, 60)
    d, h             = divmod(h, 24)
    print('\nBegin time: ', begin_ctime)
    print('End   time: ', end_ctime,'\n')
    print("Time taken: {0:.0f} days, {1:.0f} hours, \
          {2:.0f} minutes, {3:f} seconds.".format(d, h, m, s))



