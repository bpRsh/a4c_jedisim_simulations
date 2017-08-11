#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Ian Dell Antonio ; Professor, Brown University,et. al.
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
#
# Date        : Jul 8, 2013
# Last update : Aug 11, 2016
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
# Estimated time : 5 hours
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



# create config dictionary
config_path= 'physics_settings/config0.conf'
config0 = config_dict(config_path)

# print config dictionary
#for k, v in config.items(): print(k, v)

# make copy
config_record = copy.deepcopy(config0)




##==============================================================================
## make the filenames from the config parameters
##==============================================================================
print(config0['HST_image'])  # HST.fits
prefix = config0['output_folder'] + config0['prefix']  #


keys = ['HST_image',            'HST_convolved_image',
        'LSST_convolved_image', 'LSST_convolved_noise_image',
        'catalog_file',         'dislist_file',
        'distortedlist_file',   'convolvedlist_file'  ]


for i in range(len(keys)):
    key = keys[i]
    config0[key] = prefix + config0[key]

print(config0['HST_image'])  # jedisim_out/out0/trial0_HST.fits


# list of psf and outfile
psf,outfile     = [], []
with open(config0['psf_file'],"r")    as f: psf     = f.readlines()
with open(config0['output_file'],"r") as f: outfile = f.readlines()

# print for checking
print(psf[0])      # psf/psf0.fits
print(outfile[0])  # jedisim_out/rescaled_convolved_lsst_out0/rescaled_convolved_lsst_0.fits



def jedicolor_jedicatalog(i):

    ##==============================================================================
    # Depends: ~/jedisim/simdatabase/colors/*.fits
    # Creates: jedisim_out/color_out/color_out/blue_red_0_to100.fits as from color.txt
    # jedicatalog and jeditransform needs these fitsfiles
    # generate_color_txt will create outfolders
    run_process("jedicolor ", ['./executables/jedicolor', \
                    'jedisim_out/color_out/color{:d}.txt'.format(i), \
                    '1.0' ])




    # make the catalog of galaxies
    # Depends: physics_settings: config0.conf, lens.txt, psf.txt
    #          jedisim_out: out0
    #          simdatabase: radius_db, red_db
    #          jedisim_out: color_out/color_out/blue_red_0_to_100.fits
    # Creates: jedisim_out/out0: trial0_catalog.txt, trial0_convolvedlist.txt, trial0_distortedlist.txt
    out = 'jedisim_out/out{:d}'.format(i)
    replace_outfolder(out)
    run_process("jedicatalog", ["./executables/jedicatalog",\
                'physics_settings/config{:d}.conf'.format(i) ])





# run in parallel
results = Parallel(n_jobs=-1)(delayed(jedicolor_jedicatalog)(i) for i in range(4))





##==============================================================================
##==============================================================================
def jedisim_loop(low,high,core_num):
    """ Arguments:
        low,high = limits, eg. 0-5 or 5-10 or 10-15 or 15-21
        core_num = 0,1,2 or 3
    """

    for i in range(low,high):

        # Depends: ~/jedisim/simdatabase/colors/*.fits
        #          jedisim_out/color_out/color0.txt
        #          jedisim_out/color_out/color_out0 will be replaced, not the color0.txt

        # Creates: jedisim_out/color_out/color_out0/blue_red_0_to100.fits as from color0.txt
        # jedicatalog and jeditransform need these fitsfiles
        out = 'jedisim_out/color_out/color_out{:d}'.format(core_num)
        replace_outfolder(out)

        run_process("jedicolor", ['./executables/jedicolor',\
          "jedisim_out/color_out/color{:d}.txt".format(core_num),\
           str(i/20.0)])




        # run jeditransform
        # Depends     : 1. jedisim_out/color_out/color_out0/blue_red_*.fits
        #               2. jedisim_out/out0/trial0_catalog.txt
        #               3. jedisim_out/out0/stamp_0/stamp_0_to12  # 13 empty output folders
        #
        #
        # Outputs     : 1. 12,420 zipped stamps
        #                  e.g. jedisim_out/out0/stamp_0/stamp_0.fits.gz  (stamp_0 to stamp_12)
        #               2. jedisim_out/out0/trial_0/trial0_dislist.txt
        for j in range(13):

            #e.g.  jedisim_out/out0/stamp_0
            out = 'jedisim_out/out{:d}/stamp_{:d}'.format(core_num,j)
            replace_outfolder(out)

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
        for k in range(13):
            out = 'jedisim_out/out{:d}/distorted_{:d}'.format(core_num,k)
            replace_outfolder(out)

        run_process("jedidistort ", ['./executables/jedidistort', \
                    '12288', \
                    '12288', \
                    'jedisim_out/out{:d}/trial0_dislist.txt'.format(core_num), \
                    'physics_settings/lens.txt', \
                    '0.03', \
                    '0.3' ])




        # combine the lensed galaxies onto one large image
        # Depends     : 1. config file for nx,ny,distortedlist,HST
        #               2. jedisim_out/out0/trial0_distortedlist.txt
        #               3. jedisim_out/out0/distorted_0_to12/distorted_0_to_12419.fits
        #
        #
        # Output      : 1. jedisim_out/out0/trial0_HST.fits
        out = 'jedisim_out/out{:d}/trial0_HST.fits'.format(core_num)
        if os.path.exists(out): os.remove(out)

        run_process("jedipaste ", ['./executables/jedipaste', \
                    '12288', \
                    '12288', \
                    'jedisim_out/out{:d}/trial0_distortedlist.txt'.format(core_num), \
                    'jedisim_out/out{:d}/trial0_HST.fits'.format(core_num) ])




        # Convonlve the large HST image with the PSF
        # This creates 6 bands of the image for convolved HST image
        # Depends     : 1. fitsfile_to_convolve : jedisim_out/out0/trial0_HST.fits
        #               2. psf_to_convolve_with : psf/psf0.fits
        #               3. output_path_to_write_6_bands: jedisim_out/out0/convolved
        #
        #
        # Output      : 1. jedisim_out/out0/convolved/convolved_band_0_to_5.fits : 6 convolved band
        out = 'jedisim_out/out{:d}/convolved'.format(core_num)
        replace_outfolder(out)

        run_process("jediconvolve", ['./executables/jediconvolve',\
          'jedisim_out/out{:d}/trial0_HST.fits'.format(core_num),\
           psf[i],\
          'jedisim_out/out{:d}/convolved/'.format(core_num)   ])




        # Combine six bands into a single image
        # Depends     : 1. config file for nx,ny,convolvedlist,HST
        #               2. jedisim_out/out0/trial0_convolvedlist.txt
        #               3. jedisim_out/out0/convolved/convolved_band_0_to_5.fits
        #
        #
        # Output      : 1. jedisim_out/out0/trial0_HST.fits
        out = 'jedisim_out/out{:d}/trial0_HST_convolved.fits'.format(core_num)
        if os.path.exists(out): os.remove(out)

        run_process("jedipaste", ['./executables/jedipaste',\
          config0['nx'],\
          config0['ny'],\
          'jedisim_out/out{:d}/trial0_convolvedlist.txt'.format(core_num)   ,\
          'jedisim_out/out{:d}/trial0_HST_convolved.fits'.format(core_num)     ])




        # Scale the image down from HST to LSST scale and trim the edges
        # Inputs      : 1. jedisim_out/out0/trial0_HST_convolved.fits
        #
        #
        # Outputs     : 1. jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits
        # do not replace, but create outfolder if does not exist.
        out = 'jedisim_out/rescaled_convolved_lsst_out'
        if not os.path.exists(out): os.makedirs(out)

        run_process("jedirescale", ['./executables/jedirescale',\
          'jedisim_out/out{:d}/trial0_HST_convolved.fits'.format(core_num)    ,\
          config0['pix_scale'],\
          config0['final_pix_scale'],\
          config0['x_trim'],\
          config0['y_trim'],\
          'jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits'.format(i)  ])



# run that function
args = [ [0,5,0], [5,10,1], [10,16,2], [16,21,3]    ]
results = Parallel(n_jobs=-1)(delayed(jedisim_loop)(i,j,k) for i,j,k in args)




## average the 21 fits files from : jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_{:d}.fits
## and write to : jedisim_out/averaged_lsst/lsst_0_unnoised.fits
## Depends: jedisim_out/rescaled_convolved_lsst_21/rescaled_convolved_lsst_0_to20.fits
##          as from physics_settings/rescaled_convolved_lsst_21.txt
## Creates: jedisim_out/averaged_lsst/lsst_0_unnoised.fits
## do not replace, create only if non-existent
outfolder = 'jedisim_out/averaged_lsst'
if not os.path.exists(outfolder): os.makedirs(outfolder)

run_process("jediaverage",['./executables/jediaverage',
    'physics_settings/rescaled_convolved_lsst_21.txt',
    'jedisim_out/averaged_lsst/lsst_0_unnoised.fits' ])






# simulate exposure time and add Poisson noise
# Depends: jedisim_out/averaged_lsst/lsst_0_unnoised.fits
# Creates: jedisim_out/averaged_lsst_noised/lsst_0.fits

## do not replace, create only if non-existent
outfolder = 'jedisim_out/averaged_lsst_noised'
if not os.path.exists(outfolder): os.makedirs(outfolder)

run_process("jedinoise", ['./executables/jedinoise',
    'jedisim_out/averaged_lsst/lsst_0_unnoised.fits',
    '6000',
    '10',
    'jedisim_out/averaged_lsst_noised/lsst_0.fits'])




# add noise to aout/aout10.fits and choose this as monochromatic psf
# Depends: jedisim_out/rescaled_convolved_lsst_21/rescaled_convolved_lsst_10.fits
# Creates: jedisim_out/noised_monochromatic/mono.fits
run_process("jedinoise", ['./executables/jedinoise',
    'jedisim_out/rescaled_convolved_lsst_21/rescaled_convolved_lsst_10.fits',
    config0['exp_time'],
    config0['noise_mean'],
    'jedisim_out/noised_monochromatic/mono.fits'])




# success
print("jedisim successful! Exiting.")

