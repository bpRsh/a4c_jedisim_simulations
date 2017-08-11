#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Aug 01, 2016
# Last update : Aug 15, 2016

# Inputs      : jedimaster.py, especially the final outputs
#               out1/trial0_LSST_convolved_noise.fits
#               out1/90_trial0_LSST_convolved_noise.fits
# 
# Outputs     : jedisim_output/lsst*.fits
#               jedisim_output/90_lsst*.fits
#               jedisim_output/aout10_noise*.fits
#               jedisim_output/90_aout10_noise*.fits

# Info:
# 1. This is a wrapper script to jedimaster.py.
#    Basically it copies the final outputs of jedimaster to a different
#    directory in each loop.
#
# Estimated time : one loop takes 4 hours (mac)
#                  one loop takes 6 hour 20 minutes (linux)
#

# Imports
from __future__ import print_function
import os
import sys
import subprocess
import math
import re
import shutil
import copy
import time

# start time
start_time = time.time()
start_ctime = time.ctime()

##======================================================================
##======================================================================
# function to run a program and write output to the shell
def run_process(name, args,):
    print("------------------------------------------")
    print("Running: %s\nCommand:"%name)
    for arg in args:
        print(arg, end=' ')
    print("")
    print("------------------------------------------")

    subprogram_start_time = time.time()
    process = subprocess.Popen(args)

    process.communicate()
    if process.returncode != 0:
        print("Error: %s did not terminate correctly. \
        Return code: %i."%(name, process.returncode))
        sys.exit(1)


    subprogram_end_time = time.time()
    sec  = subprogram_end_time - subprogram_start_time
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print("\nTime for'{}' ==> {:2.0f} days, {:2.0f} hr,\
         {:2.0f} min, {:f} sec.".format( name, d, h, m, s))
    
    print("End of command: %s\nCommand:"%name)
    print("------------------------------------------------\n")

##======================================================================
##======================================================================

# create outfolder names
outfolder  = 'jedisim_output/jedisim_output' + time.strftime("_%b_%d_%H_%M/")

if not os.path.exists(outfolder):
    os.makedirs(outfolder)


NUM_LOOP = 2
start    = 23
end      = start + NUM_LOOP
# run jedimaster in a loop
for i in range(start,end):
    print('{} {} {}'.format('Running jemaster loop :',i, ''))

    run_process("jedimaster.py",['python',
      "jedimaster.py", "physics_settings/config1.conf"  ])


    # copy final output files
    infile1  = r'out1/trial0_LSST_convolved_noise.fits'
    outfile1 = outfolder + 'lsst_{:d}.fits'.format(i)
    
    infile2  = r'90_out1/90_trial0_LSST_convolved_noise.fits'
    outfile2 = outfolder + '90_lsst_{:d}.fits'.format(i)
    
    infile3  = r'aout/aout10_noise.fits'
    outfile3 = outfolder + 'monochromatic_{:d}.fits'.format(i)
    
    infile4  = r'aout/90_aout10_noise.fits'
    outfile4 = outfolder + '90_monochromatic_{:d}.fits'.format(i)
    

    
    shutil.copyfile(infile1, outfile1)
    shutil.copyfile(infile2, outfile2)
    shutil.copyfile(infile3, outfile3)
    shutil.copyfile(infile4, outfile4)

   
    print('{} {} {}'.format('!'*80,'', ''))
    print('{} {} {} {}'.format('!'*35,' End of jedimaster loop :',i, '!'*35))
    print('{} {} {}'.format('!'*80,'\n', ''))


# print the time taken
end_time = time.time()
seconds  = end_time - start_time
m, s     = divmod(seconds, 60)
h, m     = divmod(m, 60)
d, h     = divmod(h, 24)
print('{} {} {}'.format('Begin time: ',start_ctime, ''))
print('{} {} {}'.format('End   time: ',time.ctime(), ''))
print("\nTime taken ==> {:2.0f} days, {:2.0f} hours,\
{:2.0f} minutes, {:f} seconds.".format( d, h, m, s))
