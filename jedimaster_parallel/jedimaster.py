#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Ian Dell Antonio ; Professor, Brown University,et. al.
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
#
# Date        : Jul 8, 2013
# Last update : Aug 11, 2016
# Updated     : Sep 19, 2016
#
# Inputs      : 1. executables/*
#               2. physics_settings/out.txt_90_out.txt_color.txt_psf.txt_lens.txt
#               3. psf/*
#               4. simdatabase/*
#
# Outputs     : 1. aout    # final psf outpuf folder
#             : 2. out1    # outputs from executables
#             : 3. 90_out1 # 90 degree rotated case
#
# Final output: out1/trial0_LSST_convolved_noise.fits
#               out1/90_trial0_LSST_convolved_noise.fits
#
#
# Info:
# 1. jedicolor
#    This prgoram takes in 101 blue galaxies ( simdatabase/colors/f606w_gal*.fits)
#                          101 red galaxies( simdatabase/colors/f814w_gal*.fits)
#            and then, pix3[ii] = ((1-m)*pix1[ii])+(m*pix2[ii]); with m = 1 at first.
#
#            This creates 101 galaxies inside simdatabase/f1/out*.fits
#
# 2. jedicatalog
# This program takes in : config1.conf,lens.txt,psf.txt, config_ouptput_folder,
#                         simdatabase/radius_db, simdatabase/red_db, simdatabase/f1/*.fits
#
#    And, creates       : config_output_folder/trial0_catalog.txt,
#                         config_output_folder/trial0_convolvedlist.txt
#                         config_output_folder/trial0_distortedlist.txt
# 3. jedicolor
#     Inside the loop this program does:
#       'jedicolor',  "physics_settings/color.txt",str(x/20.0)]
#
# 4. jeditransform
#       jeditransform, config['catalog_file'],config['dislist_file']])
#
#
#
#
#
# !!WARNING!! This program will clobber the folders : aout, out1, 90_out1, simdatabase/f1
#
#
# Estimated time : 6 hours
# Command        : python3 jedimaster.py physics_settings/config1.conf

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
from generate_color_txt import generate_color_txt
from multiprocessing import Process
from joblib import Parallel, delayed
import time

# beginning time
program_begin_time = time.time()
begin_ctime        = time.ctime()





##==============================================================================
## Parallel programming
##==============================================================================
def runInParallel(*fns):

    # import
    from multiprocessing import Process

    # processes
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()











##==============================================================================
## replace_outfolder
##==============================================================================
def replace_outfolder(outfolder):

    # imports
    import shutil,os

    if os.path.exists(outfolder):
        print('Replacing folder: ', outfolder)
        shutil.rmtree(outfolder)
        os.makedirs(outfolder)
    else:
        print('Making new folder: ', outfolder)
        os.makedirs(outfolder)





##==============================================================================
## config_dict
##==============================================================================
def config_dict(config_path):

    # imports
    import re

    # parse config file and make a dictionary
    with open (config_path,'r') as f:
        config = {}
        string_regex = re.compile('"(.*?)"')
        value_regex = re.compile('[^ |\t]*')

        for line in f:
            if not line.startswith("#"):
                temp = []
                temp = line.split("=")
                if temp[1].startswith("\""):
                    config[temp[0]] = string_regex.findall(temp[1])[0]
                else:
                    config[temp[0]] = value_regex.findall(temp[1])[0]
    return config







###=============================================================================
## run process
###=============================================================================
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





def jedicolor_jedicatalog(core_num):

    ##==============================================================================
    # Depends: simdatabase/colors/*.fits
    #          physics_settings/color0.txt_upto_3.txt  # created externally
    #          jedisim_out/color_out/color_out0_to3        # empty folders
    #
    # Creates: jedisim_out/color_out/color_out0/blue_red_0_to100.fits as from color.txt
    # jedicatalog and jeditransform needs these fitsfiles
    # generate_color_txt will create outfolders
    run_process("jedicolor ", ['./executables/jedicolor', \
                    'physics_settings/color{:d}.txt'.format(core_num), \
                    '1.0' ])




    # make the catalog of galaxies
    # Depends: physics_settings: config0.conf, lens.txt, psf.txt
    #          jedisim_out: out0
    #          simdatabase: radius_db, red_db
    #          jedisim_out: color_out/color_out/blue_red_0_to_100.fits
    #
    # Creates: jedisim_out/out0: trial0_catalog.txt, trial0_convolvedlist.txt, trial0_distortedlist.txt
    run_process("jedicatalog", ["./executables/jedicatalog",\
                'physics_settings/config{:d}.conf'.format(core_num) ])









##==============================================================================
## Creating outfolders
##==============================================================================
out1 = 'jedisim_out/rescaled_convolved_lsst_out'
out2 = 'jedisim_out/hst'
if not os.path.exists(out1): os.makedirs(out1)
if not os.path.exists(out2): os.makedirs(out2)

# Creating four folders
for core_num in range(4):
    out = 'jedisim_out/color_out/color_out{:d}'.format(core_num)
    replace_outfolder(out)

    out = 'jedisim_out/out{:d}'.format(core_num)
    replace_outfolder(out)

    out = 'jedisim_out/out{:d}/convolved'.format(core_num)
    replace_outfolder(out)


# Creating 13 folders
for core_num in range(4):
    for j in range(13):
        out = 'jedisim_out/out{:d}/stamp_{:d}'.format(core_num,j)
        replace_outfolder(out)

        out = 'jedisim_out/out{:d}/distorted_{:d}'.format(core_num,j)
        replace_outfolder(out)








##==============================================================================
## Create catalogs inside FOUR folders
##==============================================================================

def func1(): jedicolor_jedicatalog(core_num = 0)
def func2(): jedicolor_jedicatalog(core_num = 1)
def func3(): jedicolor_jedicatalog(core_num = 2)
def func4(): jedicolor_jedicatalog(core_num = 3)
runInParallel(func1, func2,func3,func4)
# catalog.txt looks like this
#jedisim_out/color_out/color_out0/blue_red_39.fits  9988.295898 8329.549805
#245.445786 1.500000    0.030000    24.608101   0.181500    27.139999   0.094200





##==============================================================================
##==============================================================================
def func1():
    low = 0
    high = 5
    core_num = 0
    for loop_num in range(low,high):

        # Depends: simdatabase/colors/blue_and_red_galaxies.fits
        #          physics_settings/color0.txt
        #
        # Creates: jedisim_out/color_out/color_out0/blue_red_0_to100.fits as from color0.txt
        # jedicatalog and jeditransform need these fitsfiles
        outfolder = 'jedisim_out/color_out/color_out{:d}'.format(core_num)
        replace_outfolder(outfolder)
        run_process("jedicolor", ['./executables/jedicolor',\
          "physics_settings/color{:d}.txt".format(core_num),\
           str(loop_num/20.0)])




        # run jeditransform
        # Depends     : 1. jedisim_out/color_out/color_out0/blue_red_*.fits
        #               2. jedisim_out/out0/trial0_catalog.txt
        #               3. jedisim_out/out0/stamp_0/stamp_0_to12  # 13 empty output folders
        #
        #
        # Outputs     : 1. 12,420 zipped stamps
        #                  e.g. jedisim_out/out0/stamp_0/stamp_0.fits.gz  (stamp_0 to stamp_12)
        #               2. jedisim_out/out0/trial_0/trial0_dislist.txt
        for ii in range(13):
            outfolder = 'jedisim_out/out{:d}/stamp_{:d}'.format(core_num,ii)
            replace_outfolder(outfolder)
        # now run jeditransform
        run_process("jeditransform ", ['./executables/jeditransform', \
                     'jedisim_out/out{:d}/trial0_catalog.txt'.format(core_num), \
                     'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num) ])




        # lens the galaxies one at a time
        # Depends     : 1. jedisim_out/out0/trial0_dislist.txt
        #               2. physics_settings/lens.txt
        #               3. jedisim_out/out0/stamp_0_to_12/stamp_0_to_999.fits.gz ( 12420 input zipped galaxies)
        #               4. jedisim_out/out0/distorted_0_to_12/  ( 13 empty folder to write unzipped distorted galaxies)
        #
        #
        # Creates     : 1. jedisim_out/out0/distorted_0_to_12/distorted_0_to_12419.fits
        for ii in range(13):
            outfolder = 'jedisim_out/out{:d}/distorted_{:d}'.format(core_num,ii)
            replace_outfolder(outfolder)
        # now run jedidistort
        run_process("jedidistort ", ['./executables/jedidistort', \
                    '12288', \
                    '12288', \
                    'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num), \
                    'physics_settings/lens.txt', \
                    '0.03', \
                    '0.3' ])




        # combine the 12,420 distorted galaxies onto one large image
        # Depends     : 1. config file for nx,ny,distortedlist,HST
        #               2. jedisim_out/out0/trial0_distortedlist.txt
        #               3. jedisim_out/out0/distorted_0_to12/distorted_0_to_12419.fits
        #
        #
        # Output      : 1. jedisim_out/hst/trial0_HST_0.fits
        run_process("jedipaste ", ['./executables/jedipaste', \
                    '12288', \
                    '12288', \
                    'jedisim_out/out{:d}/trial0_distortedlist.txt'.format(core_num), \
                    'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num) ])




        # Convonlve the large HST image with the PSF
        # This creates 6 bands of the image for convolved HST image
        # Depends     : 1. fitsfile_to_convolve : jedisim_out/hst/trial0_HST_0.fits
        #               2. psf_to_convolve_with : psf/psf0.fits
        #               3. output_path_to_write_6_bands: jedisim_out/out0/convolved
        #
        #
        # Output      : 1. jedisim_out/out0/convolved/convolved_band_0_to_5.fits : 6 convolved band
        outfolder = 'jedisim_out/out{:d}/convolved'.format(core_num)
        replace_outfolder(outfolder)
        run_process("jediconvolve", ['./executables/jediconvolve',\
          'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num),\
           'psf/psf{:d}.fits'.format(loop_num),\
          'jedisim_out/out{:d}/convolved/'.format(core_num)   ])




        # Combine six bands into a single image
        # Depends     : 1. config file for nx,ny,convolvedlist,HST
        #               2. jedisim_out/out0/trial0_convolvedlist.txt
        #               3. jedisim_out/out0/convolved/convolved_band_0_to_5.fits
        #
        #
        # Output      : 1. jedisim_out/hst/trial0_HST_convolved_0.fits
        run_process("jedipaste", ['./executables/jedipaste',\
          '12288',\
          '12288',\
          'jedisim_out/out{:d}/trial0_convolvedlist.txt'.format(core_num)   ,\
          'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)     ])




        # Scale the image down from HST to LSST scale and trim the edges
        # Inputs      : 1. jedisim_out/hst/trial0_HST_convolved_0.fits
        #
        #
        # Outputs     : 1. jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits
        # do not replace, but create outfolder if does not exist
        outfolder = 'jedisim_out/rescaled_convolved_lsst_out'
        if not os.path.exists(outfolder): os.makedirs(outfolder)
        run_process("jedirescale", ['./executables/jedirescale',\
          'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)   ,\
          '0.03',\
          '0.2',\
          '480',\
          '480',\
          'jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits'.format(loop_num)  ])

        # now we can delete hst image to save space since we need only lsst image
        hst1 = 'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num)
        hst2 = 'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)
        os.remove(hst1)
        os.remove(hst2)
##==============================================================================
##==============================================================================
##==============================================================================
def func2():
    low = 5
    high = 10
    core_num = 1
    for loop_num in range(low,high):

        # Depends: simdatabase/colors/blue_and_red_galaxies.fits
        #          physics_settings/color0.txt
        #
        # Creates: jedisim_out/color_out/color_out0/blue_red_0_to100.fits as from color0.txt
        # jedicatalog and jeditransform need these fitsfiles
        outfolder = 'jedisim_out/color_out/color_out{:d}'.format(core_num)
        replace_outfolder(outfolder)
        run_process("jedicolor", ['./executables/jedicolor',\
          "physics_settings/color{:d}.txt".format(core_num),\
           str(loop_num/20.0)])




        # run jeditransform
        # Depends     : 1. jedisim_out/color_out/color_out0/blue_red_*.fits
        #               2. jedisim_out/out0/trial0_catalog.txt
        #               3. jedisim_out/out0/stamp_0/stamp_0_to12  # 13 empty output folders
        #
        #
        # Outputs     : 1. 12,420 zipped stamps
        #                  e.g. jedisim_out/out0/stamp_0/stamp_0.fits.gz  (stamp_0 to stamp_12)
        #               2. jedisim_out/out0/trial_0/trial0_dislist.txt
        for ii in range(13):
            outfolder = 'jedisim_out/out{:d}/stamp_{:d}'.format(core_num,ii)
            replace_outfolder(outfolder)
        # now run jeditransform
        run_process("jeditransform ", ['./executables/jeditransform', \
                     'jedisim_out/out{:d}/trial0_catalog.txt'.format(core_num), \
                     'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num) ])




        # lens the galaxies one at a time
        # Depends     : 1. jedisim_out/out0/trial0_dislist.txt
        #               2. physics_settings/lens.txt
        #               3. jedisim_out/out0/stamp_0_to_12/stamp_0_to_999.fits.gz ( 12420 input zipped galaxies)
        #               4. jedisim_out/out0/distorted_0_to_12/  ( 13 empty folder to write unzipped distorted galaxies)
        #
        #
        # Creates     : 1. jedisim_out/out0/distorted_0_to_12/distorted_0_to_12419.fits
        for ii in range(13):
            outfolder = 'jedisim_out/out{:d}/distorted_{:d}'.format(core_num,ii)
            replace_outfolder(outfolder)
        # now run jedidistort
        run_process("jedidistort ", ['./executables/jedidistort', \
                    '12288', \
                    '12288', \
                    'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num), \
                    'physics_settings/lens.txt', \
                    '0.03', \
                    '0.3' ])




        # combine the 12,420 distorted galaxies onto one large image
        # Depends     : 1. config file for nx,ny,distortedlist,HST
        #               2. jedisim_out/out0/trial0_distortedlist.txt
        #               3. jedisim_out/out0/distorted_0_to12/distorted_0_to_12419.fits
        #
        #
        # Output      : 1. jedisim_out/hst/trial0_HST_0.fits
        run_process("jedipaste ", ['./executables/jedipaste', \
                    '12288', \
                    '12288', \
                    'jedisim_out/out{:d}/trial0_distortedlist.txt'.format(core_num), \
                    'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num) ])




        # Convonlve the large HST image with the PSF
        # This creates 6 bands of the image for convolved HST image
        # Depends     : 1. fitsfile_to_convolve : jedisim_out/hst/trial0_HST_0.fits
        #               2. psf_to_convolve_with : psf/psf0.fits
        #               3. output_path_to_write_6_bands: jedisim_out/out0/convolved
        #
        #
        # Output      : 1. jedisim_out/out0/convolved/convolved_band_0_to_5.fits : 6 convolved band
        outfolder = 'jedisim_out/out{:d}/convolved'.format(core_num)
        replace_outfolder(outfolder)
        run_process("jediconvolve", ['./executables/jediconvolve',\
          'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num),\
           'psf/psf{:d}.fits'.format(loop_num),\
          'jedisim_out/out{:d}/convolved/'.format(core_num)   ])




        # Combine six bands into a single image
        # Depends     : 1. config file for nx,ny,convolvedlist,HST
        #               2. jedisim_out/out0/trial0_convolvedlist.txt
        #               3. jedisim_out/out0/convolved/convolved_band_0_to_5.fits
        #
        #
        # Output      : 1. jedisim_out/hst/trial0_HST_convolved_0.fits
        run_process("jedipaste", ['./executables/jedipaste',\
          '12288',\
          '12288',\
          'jedisim_out/out{:d}/trial0_convolvedlist.txt'.format(core_num)   ,\
          'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)     ])




        # Scale the image down from HST to LSST scale and trim the edges
        # Inputs      : 1. jedisim_out/hst/trial0_HST_convolved_0.fits
        #
        #
        # Outputs     : 1. jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits
        # do not replace, but create outfolder if does not exist
        outfolder = 'jedisim_out/rescaled_convolved_lsst_out'
        if not os.path.exists(outfolder): os.makedirs(outfolder)
        run_process("jedirescale", ['./executables/jedirescale',\
          'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)   ,\
          '0.03',\
          '0.2',\
          '480',\
          '480',\
          'jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits'.format(loop_num)  ])

        # now we can delete hst image to save space since we need only lsst image
        hst1 = 'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num)
        hst2 = 'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)
        os.remove(hst1)
        os.remove(hst2)
##==============================================================================
##==============================================================================
##==============================================================================
def func3():
    low = 10
    high = 15
    core_num = 2
    for loop_num in range(low,high):

        # Depends: simdatabase/colors/blue_and_red_galaxies.fits
        #          physics_settings/color0.txt
        #
        # Creates: jedisim_out/color_out/color_out0/blue_red_0_to100.fits as from color0.txt
        # jedicatalog and jeditransform need these fitsfiles
        outfolder = 'jedisim_out/color_out/color_out{:d}'.format(core_num)
        replace_outfolder(outfolder)
        run_process("jedicolor", ['./executables/jedicolor',\
          "physics_settings/color{:d}.txt".format(core_num),\
           str(loop_num/20.0)])




        # run jeditransform
        # Depends     : 1. jedisim_out/color_out/color_out0/blue_red_*.fits
        #               2. jedisim_out/out0/trial0_catalog.txt
        #               3. jedisim_out/out0/stamp_0/stamp_0_to12  # 13 empty output folders
        #
        #
        # Outputs     : 1. 12,420 zipped stamps
        #                  e.g. jedisim_out/out0/stamp_0/stamp_0.fits.gz  (stamp_0 to stamp_12)
        #               2. jedisim_out/out0/trial_0/trial0_dislist.txt
        for ii in range(13):
            outfolder = 'jedisim_out/out{:d}/stamp_{:d}'.format(core_num,ii)
            replace_outfolder(outfolder)
        # now run jeditransform
        run_process("jeditransform ", ['./executables/jeditransform', \
                     'jedisim_out/out{:d}/trial0_catalog.txt'.format(core_num), \
                     'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num) ])




        # lens the galaxies one at a time
        # Depends     : 1. jedisim_out/out0/trial0_dislist.txt
        #               2. physics_settings/lens.txt
        #               3. jedisim_out/out0/stamp_0_to_12/stamp_0_to_999.fits.gz ( 12420 input zipped galaxies)
        #               4. jedisim_out/out0/distorted_0_to_12/  ( 13 empty folder to write unzipped distorted galaxies)
        #
        #
        # Creates     : 1. jedisim_out/out0/distorted_0_to_12/distorted_0_to_12419.fits
        for ii in range(13):
            outfolder = 'jedisim_out/out{:d}/distorted_{:d}'.format(core_num,ii)
            replace_outfolder(outfolder)
        # now run jedidistort
        run_process("jedidistort ", ['./executables/jedidistort', \
                    '12288', \
                    '12288', \
                    'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num), \
                    'physics_settings/lens.txt', \
                    '0.03', \
                    '0.3' ])




        # combine the 12,420 distorted galaxies onto one large image
        # Depends     : 1. config file for nx,ny,distortedlist,HST
        #               2. jedisim_out/out0/trial0_distortedlist.txt
        #               3. jedisim_out/out0/distorted_0_to12/distorted_0_to_12419.fits
        #
        #
        # Output      : 1. jedisim_out/hst/trial0_HST_0.fits
        run_process("jedipaste ", ['./executables/jedipaste', \
                    '12288', \
                    '12288', \
                    'jedisim_out/out{:d}/trial0_distortedlist.txt'.format(core_num), \
                    'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num) ])




        # Convonlve the large HST image with the PSF
        # This creates 6 bands of the image for convolved HST image
        # Depends     : 1. fitsfile_to_convolve : jedisim_out/hst/trial0_HST_0.fits
        #               2. psf_to_convolve_with : psf/psf0.fits
        #               3. output_path_to_write_6_bands: jedisim_out/out0/convolved
        #
        #
        # Output      : 1. jedisim_out/out0/convolved/convolved_band_0_to_5.fits : 6 convolved band
        outfolder = 'jedisim_out/out{:d}/convolved'.format(core_num)
        replace_outfolder(outfolder)
        run_process("jediconvolve", ['./executables/jediconvolve',\
          'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num),\
           'psf/psf{:d}.fits'.format(loop_num),\
          'jedisim_out/out{:d}/convolved/'.format(core_num)   ])




        # Combine six bands into a single image
        # Depends     : 1. config file for nx,ny,convolvedlist,HST
        #               2. jedisim_out/out0/trial0_convolvedlist.txt
        #               3. jedisim_out/out0/convolved/convolved_band_0_to_5.fits
        #
        #
        # Output      : 1. jedisim_out/hst/trial0_HST_convolved_0.fits
        run_process("jedipaste", ['./executables/jedipaste',\
          '12288',\
          '12288',\
          'jedisim_out/out{:d}/trial0_convolvedlist.txt'.format(core_num)   ,\
          'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)     ])




        # Scale the image down from HST to LSST scale and trim the edges
        # Inputs      : 1. jedisim_out/hst/trial0_HST_convolved_0.fits
        #
        #
        # Outputs     : 1. jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits
        # do not replace, but create outfolder if does not exist
        outfolder = 'jedisim_out/rescaled_convolved_lsst_out'
        if not os.path.exists(outfolder): os.makedirs(outfolder)
        run_process("jedirescale", ['./executables/jedirescale',\
          'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)   ,\
          '0.03',\
          '0.2',\
          '480',\
          '480',\
          'jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits'.format(loop_num)  ])

        # now we can delete hst image to save space since we need only lsst image
        hst1 = 'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num)
        hst2 = 'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)
        os.remove(hst1)
        os.remove(hst2)
##==============================================================================
##==============================================================================
##==============================================================================
def func4():
    low = 15
    high = 21
    core_num = 3
    for loop_num in range(low,high):

        # Depends: simdatabase/colors/blue_and_red_galaxies.fits
        #          physics_settings/color0.txt
        #
        # Creates: jedisim_out/color_out/color_out0/blue_red_0_to100.fits as from color0.txt
        # jedicatalog and jeditransform need these fitsfiles
        outfolder = 'jedisim_out/color_out/color_out{:d}'.format(core_num)
        replace_outfolder(outfolder)
        run_process("jedicolor", ['./executables/jedicolor',\
          "physics_settings/color{:d}.txt".format(core_num),\
           str(loop_num/20.0)])




        # run jeditransform
        # Depends     : 1. jedisim_out/color_out/color_out0/blue_red_*.fits
        #               2. jedisim_out/out0/trial0_catalog.txt
        #               3. jedisim_out/out0/stamp_0/stamp_0_to12  # 13 empty output folders
        #
        #
        # Outputs     : 1. 12,420 zipped stamps
        #                  e.g. jedisim_out/out0/stamp_0/stamp_0.fits.gz  (stamp_0 to stamp_12)
        #               2. jedisim_out/out0/trial_0/trial0_dislist.txt
        for ii in range(13):
            outfolder = 'jedisim_out/out{:d}/stamp_{:d}'.format(core_num,ii)
            replace_outfolder(outfolder)
        # now run jeditransform
        run_process("jeditransform ", ['./executables/jeditransform', \
                     'jedisim_out/out{:d}/trial0_catalog.txt'.format(core_num), \
                     'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num) ])




        # lens the galaxies one at a time
        # Depends     : 1. jedisim_out/out0/trial0_dislist.txt
        #               2. physics_settings/lens.txt
        #               3. jedisim_out/out0/stamp_0_to_12/stamp_0_to_999.fits.gz ( 12420 input zipped galaxies)
        #               4. jedisim_out/out0/distorted_0_to_12/  ( 13 empty folder to write unzipped distorted galaxies)
        #
        #
        # Creates     : 1. jedisim_out/out0/distorted_0_to_12/distorted_0_to_12419.fits
        for ii in range(13):
            outfolder = 'jedisim_out/out{:d}/distorted_{:d}'.format(core_num,ii)
            replace_outfolder(outfolder)
        # now run jedidistort
        run_process("jedidistort ", ['./executables/jedidistort', \
                    '12288', \
                    '12288', \
                    'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num), \
                    'physics_settings/lens.txt', \
                    '0.03', \
                    '0.3' ])




        # combine the 12,420 distorted galaxies onto one large image
        # Depends     : 1. config file for nx,ny,distortedlist,HST
        #               2. jedisim_out/out0/trial0_distortedlist.txt
        #               3. jedisim_out/out0/distorted_0_to12/distorted_0_to_12419.fits
        #
        #
        # Output      : 1. jedisim_out/hst/trial0_HST_0.fits
        run_process("jedipaste ", ['./executables/jedipaste', \
                    '12288', \
                    '12288', \
                    'jedisim_out/out{:d}/trial0_distortedlist.txt'.format(core_num), \
                    'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num) ])




        # Convonlve the large HST image with the PSF
        # This creates 6 bands of the image for convolved HST image
        # Depends     : 1. fitsfile_to_convolve : jedisim_out/hst/trial0_HST_0.fits
        #               2. psf_to_convolve_with : psf/psf0.fits
        #               3. output_path_to_write_6_bands: jedisim_out/out0/convolved
        #
        #
        # Output      : 1. jedisim_out/out0/convolved/convolved_band_0_to_5.fits : 6 convolved band
        outfolder = 'jedisim_out/out{:d}/convolved'.format(core_num)
        replace_outfolder(outfolder)
        run_process("jediconvolve", ['./executables/jediconvolve',\
          'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num),\
           'psf/psf{:d}.fits'.format(loop_num),\
          'jedisim_out/out{:d}/convolved/'.format(core_num)   ])




        # Combine six bands into a single image
        # Depends     : 1. config file for nx,ny,convolvedlist,HST
        #               2. jedisim_out/out0/trial0_convolvedlist.txt
        #               3. jedisim_out/out0/convolved/convolved_band_0_to_5.fits
        #
        #
        # Output      : 1. jedisim_out/hst/trial0_HST_convolved_0.fits
        run_process("jedipaste", ['./executables/jedipaste',\
          '12288',\
          '12288',\
          'jedisim_out/out{:d}/trial0_convolvedlist.txt'.format(core_num)   ,\
          'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)     ])




        # Scale the image down from HST to LSST scale and trim the edges
        # Inputs      : 1. jedisim_out/hst/trial0_HST_convolved_0.fits
        #
        #
        # Outputs     : 1. jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits
        # do not replace, but create outfolder if does not exist
        outfolder = 'jedisim_out/rescaled_convolved_lsst_out'
        if not os.path.exists(outfolder): os.makedirs(outfolder)
        run_process("jedirescale", ['./executables/jedirescale',\
          'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)   ,\
          '0.03',\
          '0.2',\
          '480',\
          '480',\
          'jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits'.format(loop_num)  ])

        # now we can delete hst image to save space since we need only lsst image
        hst1 = 'jedisim_out/hst/trial0_HST_{:d}.fits'.format(loop_num)
        hst2 = 'jedisim_out/hst/trial0_HST_convolved_{:d}.fits'.format(loop_num)
        os.remove(hst1)
        os.remove(hst2)
##==============================================================================

# serial run
func1()
func2()
func3()
func4()




# Running parallel
#runInParallel(func1, func2,func3,func4)




### average the 21 fits files from : jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits
### and write to : jedisim_out/averaged_lsst/lsst_0_unnoised.fits
### Depends: jedisim_out/rescaled_convolved_lsst_21/rescaled_convolved_lsst_0_to20.fits
###          as from physics_settings/rescaled_convolved_lsst_21.txt
### Creates: jedisim_out/averaged_lsst/lsst_0_unnoised.fits
### do not replace, create only if non-existent
#outfolder = 'jedisim_out/averaged_lsst'
#if not os.path.exists(outfolder): os.makedirs(outfolder)

#run_process("jediaverage",['./executables/jediaverage',
    #'physics_settings/rescaled_convolved_lsst_21.txt',
    #'jedisim_out/averaged_lsst/lsst_0_unnoised.fits' ])






## simulate exposure time and add Poisson noise
## Depends: jedisim_out/averaged_lsst/lsst_0_unnoised.fits
## Creates: jedisim_out/averaged_lsst_noised/lsst_0.fits

### do not replace, create only if non-existent
#outfolder = 'jedisim_out/averaged_lsst_noised'
#if not os.path.exists(outfolder): os.makedirs(outfolder)

#run_process("jedinoise", ['./executables/jedinoise',
    #'jedisim_out/averaged_lsst/lsst_0_unnoised.fits',
    #'6000',
    #'10',
    #'jedisim_out/averaged_lsst_noised/lsst_0.fits'])




## add noise to aout/aout10.fits and choose this as monochromatic psf
## Depends: jedisim_out/rescaled_convolved_lsst_21/rescaled_convolved_lsst_10.fits
## Creates: jedisim_out/noised_monochromatic/mono.fits
#run_process("jedinoise", ['./executables/jedinoise',
    #'jedisim_out/rescaled_convolved_lsst_21/rescaled_convolved_lsst_10.fits',
    #config0['exp_time'],
    #config0['noise_mean'],
    #'jedisim_out/noised_monochromatic/mono.fits'])



## *****************************************************************************
##==============================================================================
## 90 degree rotated case needs catalogs from non rotated outputs
##==============================================================================
## *****************************************************************************


## Note: jedicatalog creates three text files,viz., catalog.txt, convolvedlist.txt,distortedlist.txt
## We change these files for 90 degree rotated case


#def rotated_catalogs(core_num):



    ###==============================================================================
    ### catalog.txt :  angle --> angle+90     out0 --> 90_out0   look at the bottom
    ###==============================================================================
    ## read old catalog file and rotate angle
    ## old: jedisim_out/out0/trial0_catalog.txt
    ## it has:
    ##
    ## jedisim_out/color_out/color_out0/blue_red_62.fits    3183.222412     9061.648438     185.040207
    ## input_for_jeditransform                              x               y               angle
    ##
    ##      1.500000        0.030000        23.689899       0.218280        27.730000       0.090300
    ##      redshift        pixscale        old_mag         old_rad         new_mag         new_rad
    ##
    ## jedisim_out/out0/stamp_0/stamp_0.fits.gz     jedisim_out/out0/distorted_0/distorted_0.fits
    ## stamp_to_be_created_by_jeditransform         jedidistort_will_create_these_files

    #outfolder = 'jedisim_out/90_out{:d}'.format(core_num)
    #replace_outfolder(outfolder)  # fresh start for 90 rotated case, we will write 3 text files inside it.

    #infile  = 'jedisim_out/out{:d}/trial0_catalog.txt'.format(core_num)  # it is already created
    #outfile = 'jedisim_out/90_out{:d}/90_trial0_catalog.txt'.format(core_num)

    #with open (infile,'r') as fin, open(outfile, 'w') as fout:
        #for old_line in fin:

            #l = old_line.split("\t")

            #angle = float(l[3])
            #angle2 = angle + 90.0

            #if angle2>= 360:
                #angle2 = angle2 - 360

            #l[3] = str(angle2)
            ##print('{} {} {}'.format('angle before: ',angle, ''))
            ##print('{} {} {}'.format('angle after: ',angle2, ''))
            #l[-1]= l[-1].replace('jedisim_out/out{:d}/distorted_0'.format(core_num),'jedisim_out/90_out{:d}/distorted_0'.format(core_num))

            #l[-2]= l[-2].replace('jedisim_out/out{:d}/stamp_0'.format(core_num),'jedisim_out/90_out{:d}/stamp_0'.format(core_num))
            #line = "\t".join(l)
            #fout.write(line)
        #print('Creating: ', outfile)


    ###==============================================================================
    ### convolvedlist.txt   out0 --> 90_out0
    ###==============================================================================
    ## create new convolved list from old list
    ## old     : jedisim_out/out0/trial0_convolvedlist.txt
    ## contents: jedisim_out/out0/convolved/convolved_band_0.fits_upto_5.fits
    ## needed  : jedisim_out/90_out0/convolved/convolved_band_0.fits

    #infile  = 'jedisim_out/out{:d}/trial0_convolvedlist.txt'.format(core_num)
    #outfile = 'jedisim_out/90_out{:d}/90_trial0_convolvedlist.txt'.format(core_num)
    #with open(infile,'r') as fin, open(outfile,'w') as fout:
        #for old_line in fin:
            #line = old_line.replace('out{:d}'.format(core_num),'90_out{:d}'.format(core_num))
            #fout.write(line)
        #print('Creating: ' , outfile)


    ###==============================================================================
    ### distortedlist.txt  out0 --> 90_out0
    ###==============================================================================
    ## create new distorted list from old list
    ## old      : jedisim_out/out0/trial0_distortedlist.txt
    ## contents : jedisim_out/out0/distorted_0/distorted_0.fits_upto_1000.fits
    ## needed   : jedisim_out/90_out0/distorted_0/distorted_0.fits_upto_1000.fits
    #infile  = 'jedisim_out/out{:d}/trial0_distortedlist.txt'.format(core_num)
    #outfile = 'jedisim_out/90_out{:d}/90_trial0_distortedlist.txt'.format(core_num)
    #with open(infile,'r') as fin, open(outfile,'w') as fout:

        #for old_line in fin:
            #line = old_line.replace('out{:d}'.format(core_num),'90_out{:d}'.format(core_num))
            #fout.write(line)
        #print('Creating: ', outfile)


## create 90 degree outfolders 90_out0, 90_out1, 90_out2, and 90_out3 with three textfiles inside them
#results = Parallel(n_jobs=-1)(delayed(rotated_catalogs)(core_num) for core_num in range(3))






## list of psf and outfile
#psf,outfile     = [], []
#with open(config0['psf_file'],"r")    as f: psf     = f.readlines()
#with open(config0['output_file'],"r") as f: outfile = f.readlines()

## print for checking
#print(psf[0])      # psf/psf0.fits
#print(outfile[0])  # jedisim_out/rescaled_convolved_lsst_out0/rescaled_convolved_lsst_0.fits



##def jedicolor_jedicatalog(i):

    ####==============================================================================
    ### Depends: simdatabase/colors/*.fits
    ### Creates: jedisim_out/color_out/color_out/blue_red_0_to100.fits as from color.txt
    ### jedicatalog and jeditransform needs these fitsfiles
    ### generate_color_txt will create outfolders
    ##run_process("jedicolor ", ['./executables/jedicolor', \
                    ##'jedisim_out/color_out/color{:d}.txt'.format(i), \
                    ##'1.0' ])




    ### make the catalog of galaxies
    ### Depends: physics_settings: config0.conf, lens.txt, psf.txt
    ###          jedisim_out: out0
    ###          simdatabase: radius_db, red_db
    ###          jedisim_out: color_out/color_out/blue_red_0_to_100.fits
    ### Creates: jedisim_out/out0: trial0_catalog.txt, trial0_convolvedlist.txt, trial0_distortedlist.txt
    ##out = 'jedisim_out/out{:d}'.format(i)
    ##replace_outfolder(out)
    ##run_process("jedicatalog", ["./executables/jedicatalog",\
                ##'physics_settings/config{:d}.conf'.format(i) ])





### run in parallel
##results = Parallel(n_jobs=-1)(delayed(jedicolor_jedicatalog)(i) for i in range(4))
###==============================================================================




###==============================================================================
###==============================================================================
#def jedisim_loop90(low,high,core_num):
    #""" Arguments:
        #low,high = limits, eg. 0-5 or 5-10 or 10-15 or 15-21
        #core_num = 0,1,2 or 3
    #"""

    #for i in range(low,high):

        ## Depends: simdatabase/colors/*.fits
        ##          jedisim_out/color_out/color0.txt
        ##          jedisim_out/color_out/color_out0 will be replaced, not the color0.txt

        ## Creates: jedisim_out/color_out/90_color_out0/blue_red_0_to100.fits as from color0.txt
        ## jedicatalog and jeditransform need these fitsfiles
        #out = 'jedisim_out/color_out/90_color_out{:d}'.format(core_num)
        #replace_outfolder(out)

        #run_process("jedicolor", ['./executables/jedicolor',\
          #"jedisim_out/color_out/90_color{:d}.txt".format(core_num),\
           #str(i/20.0)])




        ## run jeditransform
        ## Depends     : 1. jedisim_out/color_out/color_out0/blue_red_*.fits
        ##               2. jedisim_out/out0/trial0_catalog.txt
        ##               3. jedisim_out/out0/stamp_0/stamp_0_to12  # 13 empty output folders
        ##
        ##
        ## Outputs     : 1. 12,420 zipped stamps
        ##                  e.g. jedisim_out/out0/stamp_0/stamp_0.fits.gz  (stamp_0 to stamp_12)
        ##               2. jedisim_out/out0/trial_0/trial0_dislist.txt
        #for j in range(13):

            ##e.g.  jedisim_out/out0/stamp_0
            #out = 'jedisim_out/out{:d}/stamp_{:d}'.format(core_num,j)
            #replace_outfolder(out)

        #run_process("jeditransform ", ['./executables/jeditransform', \
                     #'jedisim_out/out{:d}/trial0_catalog.txt'.format(core_num), \
                     #'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num) ])




        ## lens the galaxies one at a time
        ## Depends     : 1. jedisim_out/out0/trial0_dislist.txt
        ##               2. physics_settings/lens.txt
        ##               3. jedisim_out/out0/stamp_0_to_12/stamp_0_to_999.fits.gz ( 12420 input zipped galaxies)
        ##               4. jedisim_out/out0/distorted_0_to_12/  ( 13 empty folder to write unzipped distorted galaxies)
        ##
        ##
        ## Creates     : 1. jedisim_out/out0/distorted_0_to_12/distorted_0_to_12419.fits
        #for k in range(13):
            #out = 'jedisim_out/out{:d}/distorted_{:d}'.format(core_num,k)
            #replace_outfolder(out)

        #run_process("jedidistort ", ['./executables/jedidistort', \
                    #'12288', \
                    #'12288', \
                    #'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num), \
                    #'physics_settings/lens.txt', \
                    #'0.03', \
                    #'0.3' ])




        ## combine the lensed galaxies onto one large image
        ## Depends     : 1. config file for nx,ny,distortedlist,HST
        ##               2. jedisim_out/out0/trial0_distortedlist.txt
        ##               3. jedisim_out/out0/distorted_0_to12/distorted_0_to_12419.fits
        ##
        ##
        ## Output      : 1. jedisim_out/out0/trial0_HST.fits
        #out = 'jedisim_out/out{:d}/trial0_HST.fits'.format(core_num)
        #if os.path.exists(out): os.remove(out)

        #run_process("jedipaste ", ['./executables/jedipaste', \
                    #'12288', \
                    #'12288', \
                    #'jedisim_out/out{:d}/trial0_distortedlist.txt'.format(core_num), \
                    #'jedisim_out/out{:d}/trial0_HST.fits'.format(core_num) ])




        ## Convonlve the large HST image with the PSF
        ## This creates 6 bands of the image for convolved HST image
        ## Depends     : 1. fitsfile_to_convolve : jedisim_out/out0/trial0_HST.fits
        ##               2. psf_to_convolve_with : psf/psf0.fits
        ##               3. output_path_to_write_6_bands: jedisim_out/out0/convolved
        ##
        ##
        ## Output      : 1. jedisim_out/out0/convolved/convolved_band_0_to_5.fits : 6 convolved band
        #out = 'jedisim_out/out{:d}/convolved'.format(core_num)
        #replace_outfolder(out)

        #run_process("jediconvolve", ['./executables/jediconvolve',\
          #'jedisim_out/out{:d}/trial0_HST.fits'.format(core_num),\
           #psf[i],\
          #'jedisim_out/out{:d}/convolved/'.format(core_num)   ])




        ## Combine six bands into a single image
        ## Depends     : 1. config file for nx,ny,convolvedlist,HST
        ##               2. jedisim_out/out0/trial0_convolvedlist.txt
        ##               3. jedisim_out/out0/convolved/convolved_band_0_to_5.fits
        ##
        ##
        ## Output      : 1. jedisim_out/out0/trial0_HST.fits
        #out = 'jedisim_out/out{:d}/trial0_HST_convolved.fits'.format(core_num)
        #if os.path.exists(out): os.remove(out)

        #run_process("jedipaste", ['./executables/jedipaste',\
          #config0['nx'],\
          #config0['ny'],\
          #'jedisim_out/out{:d}/trial0_convolvedlist.txt'.format(core_num)   ,\
          #'jedisim_out/out{:d}/trial0_HST_convolved.fits'.format(core_num)     ])




        ## Scale the image down from HST to LSST scale and trim the edges
        ## Inputs      : 1. jedisim_out/out0/trial0_HST_convolved.fits
        ##
        ##
        ## Outputs     : 1. jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits
        ## do not replace, but create outfolder if does not exist.
        #out = 'jedisim_out/rescaled_convolved_lsst_out'
        #if not os.path.exists(out): os.makedirs(out)

        #run_process("jedirescale", ['./executables/jedirescale',\
          #'jedisim_out/out{:d}/trial0_HST_convolved.fits'.format(core_num)    ,\
          #config0['pix_scale'],\
          #config0['final_pix_scale'],\
          #config0['x_trim'],\
          #config0['y_trim'],\
          #'jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits'.format(i)  ])



## run that function
#args = [ [0,5,0], [5,10,1], [10,16,2], [16,21,3]    ]
#results = Parallel(n_jobs=-1)(delayed(jedisim_loop90)(i,j,k) for i,j,k in args)




### average the 21 fits files from : jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits
### and write to : jedisim_out/averaged_lsst/lsst_0_unnoised.fits
### Depends: jedisim_out/rescaled_convolved_lsst_21/rescaled_convolved_lsst_0_to20.fits
###          as from physics_settings/rescaled_convolved_lsst_21.txt
### Creates: jedisim_out/averaged_lsst/lsst_0_unnoised.fits
### do not replace, create only if non-existent
#outfolder = 'jedisim_out/averaged_lsst'
#if not os.path.exists(outfolder): os.makedirs(outfolder)

#run_process("jediaverage",['./executables/jediaverage',
    #'physics_settings/rescaled_convolved_lsst_21.txt',
    #'jedisim_out/averaged_lsst/lsst_0_unnoised.fits' ])






## simulate exposure time and add Poisson noise
## Depends: jedisim_out/averaged_lsst/lsst_0_unnoised.fits
## Creates: jedisim_out/averaged_lsst_noised/lsst_0.fits

### do not replace, create only if non-existent
#outfolder = 'jedisim_out/averaged_lsst_noised'
#if not os.path.exists(outfolder): os.makedirs(outfolder)

#run_process("jedinoise", ['./executables/jedinoise',
    #'jedisim_out/averaged_lsst/lsst_0_unnoised.fits',
    #'6000',
    #'10',
    #'jedisim_out/averaged_lsst_noised/lsst_0.fits'])




## add noise to aout/aout10.fits and choose this as monochromatic psf
## Depends: jedisim_out/rescaled_convolved_lsst_21/rescaled_convolved_lsst_10.fits
## Creates: jedisim_out/noised_monochromatic/mono.fits
#run_process("jedinoise", ['./executables/jedinoise',
    #'jedisim_out/rescaled_convolved_lsst_21/rescaled_convolved_lsst_10.fits',
    #config0['exp_time'],
    #config0['noise_mean'],
    #'jedisim_out/noised_monochromatic/mono.fits'])





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



## success
print("jedisim successful! Exiting.")

