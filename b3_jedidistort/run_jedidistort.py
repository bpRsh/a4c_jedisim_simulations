#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 17, 2016
# Last update :
#
# Estimated time: 4 minutes for 12420 stamps

# Imports
import os,shutil
from replace_distorted import replace_distorted


def run_process(name, args,):

    '''Usage: run_process("example ", ["python ", 'example.py', 'arg1' ])    '''

    import subprocess,sys

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
    import time

    # beginning time
    program_begin_time = time.time()
    begin_ctime        = time.ctime()

    # replace old outputs
    replace_distorted()

    # run program
    # executable nx ny dislist lens  pix  redshift
    run_process("jedidistort ", ['./jedidistort', \
                '12288', \
                '12288', \
                'out1/trial0_dislist.txt', \
                'physics_settings/lens.txt', \
                '0.03', \
                '0.3' ])

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



