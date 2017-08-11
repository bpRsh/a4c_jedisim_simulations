#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 17, 2016
# Last update :
#
#  Inputs      : 1. out1/trial0_HST_convolved.fits
# 
# 
#  Outputs     : 1. out1/rescaled_convolved_lsst_0.fits
# 
# 
# 
#  Usage       : jedirescale input_file pixscale new_pixscale trimx trimy output_file
#   # scale the image down from HST to LSST scale and trim the edgescolor
#    run_process("jedirescale", ['./executables/jedirescale',
#      config['HST_convolved_image'],  # jedisim_out/out0/trial0_HST_convolved.fits
#      config['pix_scale'],            # 0.03
#      config['final_pix_scale'],      # 0.2
#      config['x_trim'],               # 480
#      config['y_trim'],               # 480
#      outfile[i]])                    # from: physics_settings/rescaled_out.txt
# 
#  Info: This program scales down convolved HST image to LSST image.
#  i.e. out1/trial0_HST_convolved.fits to out1/rescaled_convolved_lsst_0.fits
# 
# 
# 
## Estimated time: 13 sec
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
    rescaled = 'jedisim_out/out1/LSST_convolved.fits'
    if os.path.exists(rescaled):
        shutil.rmtree(rescaled)
        os.makedirs(rescaled)
    else:
        os.makedirs(rescaled)


    # run program
    # executable nx ny dislist lens  pix  redshift
    run_process("jedirescale ", ['./jedirescale', \
                'jedisim_out/out1/HST_convolved.fits', \
                '0.03', \
                '0.2', \
                '480', \
                '480', \
                'jedisim_out/out1/LSST_convolved.fits' ])

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



