#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 17, 2016
# Last update : May 09, 2017
#
# Estimated time: 3 sec

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


def main():
    # replace old outputs
    averaged = 'jedisim_out/averaged_lsst/lsst_unnoised.fits'
    if os.path.exists(averaged):
         os.remove(averaged)


    # run program
    # executable nx ny dislist lens  pix  redshift
    run_process("jediaverage ", ['./jediaverage', \
                'physics_settings/rescaled_convolved_lsst_21.txt', \
                'jedisim_out/averaged_lsst/lsst_unnoised0.fits' ])

if __name__ == '__main__':
    # beginning time
    program_begin_time = time.time()
    begin_ctime        = time.ctime()

    # run main program
    main()


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



