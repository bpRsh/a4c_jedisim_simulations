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
# Outputs     : 1. aout    # final psf output folder
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


outfolders = ['aout', 'out1', 'simdatabase/f1']
for i in range (len(outfolders)):
    outfolder = outfolders[i]
    replace_outfolder(outfolder)








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

    # imports
    import subprocess,sys,time

    # prints
    print("-------------------------------------------------")
    print("Running: %s\nCommand:"%name)
    for arg in args:
        print(arg, end=' ')
    print("")
    print("---------------------------------------------------")

    subprogram_start_time = time.time()
    process = subprocess.Popen(args)

    process.communicate()
    if process.returncode != 0:
        print("Error: %s did not terminate correctly. \
              Return code: %i."%(name, process.returncode))
        sys.exit(1)

    # print time
    subprogram_end_time = time.time()
    sec                 = subprogram_end_time - subprogram_start_time
    m, s                = divmod(sec, 60)
    h, m                = divmod(m, 60)
    d, h                = divmod(h, 24)
    print("\nTime for'{}' ==> {:2.0f} days, {:2.0f} hr,\
         {:2.0f} min, {:f} sec.".format( name, d, h, m, s))

    print("End of command: %s\nCommand:"%name)
    print("------------------------------------------------")



# create config dictionary
config_path= 'physics_settings/config.conf'
config = config_dict(config_path)

# print config dictionary
#for k, v in config.items(): print(k, v)

# make copy
config_record = copy.deepcopy(config)




##==============================================================================
## make the filenames from the config parameters
##==============================================================================
print(config['HST_image'])
prefix = config['output_folder'] + config['prefix']


keys = ['HST_image',            'HST_convolved_image',
        'LSST_convolved_image', 'LSST_convolved_noise_image',
        'catalog_file',         'dislist_file',
        'distortedlist_file',   'convolvedlist_file'  ]


for i in range(len(keys)):
    key = keys[i]
    config[key] = prefix + config[key]



# replace outfolder
outfolder = config['output_folder']
replace_outfolder(outfolder)

# replace convolved path
convolved_path = "%sconvolved/"%config['output_folder']
replace_outfolder(convolved_path)


# create stamps and distorted folders
for x in range(0, int(math.ceil(float(config['num_galaxies'])/1000))):
    postage_path = "%sstamp_%i"%(config['output_folder'],x)
    distorted_path = "%sdistorted_%i"%(config['output_folder'],x)
    if not os.path.exists(postage_path): os.makedirs(postage_path)
    if not os.path.exists(distorted_path): os.makedirs(distorted_path)



##==============================================================================
## create list of psf and outfiles
##==============================================================================
psf,outfile     = [], []
with open(config['psf_file'],"r")    as f: psf     = f.readlines()
with open(config['output_file'],"r") as f: outfile = f.readlines()

#for i in range(len(psf))    : print(psf[i],end='')
#for i in range(len(outfile)): print(outfile[i],end='')






##==============================================================================
# jedicolor creates 101 fitsfiles inside simdatabase/f1/
# jedicatalog needs this
run_process("jedicolor",['./executables/jedicolor',
          "physics_settings/color.txt",
          str(1.0) ])




# make the catalog of galaxies
run_process("jedicatalog", ["./executables/jedicatalog",
            config_path ])


##==============================================================================
##==============================================================================
for i in range(0,21):

    # jedicolor creates 101 fitsfiles inside simdatabase/f1/ as from color.txt
    run_process("jedicolor", ['./executables/jedicolor',
      "physics_settings/color.txt",
       str(i/20.0)])

    # run jeditransform
    run_process("jeditransform", ['./executables/jeditransform',
      config['catalog_file'],
      config['dislist_file']])

    # lens the galaxies one at a time
    run_process("jedidistort", ['./executables/jedidistort',
      config['nx'],
      config['ny'],
      config['dislist_file'],
      config['lenses_file'],
      config['pix_scale'],
      config['lens_z']])

    # combine the lensed galaxies onto one large image
    run_process("jedipaste", ['./executables/jedipaste',
      config['nx'],
      config['ny'],
      config['distortedlist_file'],
      config['HST_image']])

    # convonlve the large image with the PSF
    # this creates one image for each band of the image
    run_process("jediconvolve", ['./executables/jediconvolve',
      config['HST_image'],
      psf[i],
      convolved_path])

    # combine each band into a single image
    run_process("jedipaste", ['./executables/jedipaste',
      config['nx'],
      config['ny'],
      config['convolvedlist_file'],
      config['HST_convolved_image']])

    # scale the image down from HST to LSST scale and trim the edgescolor
    run_process("jedirescale", ['./executables/jedirescale',
      config['HST_convolved_image'],
      config['pix_scale'],
      config['final_pix_scale'],
      config['x_trim'],
      config['y_trim'],
      outfile[i]])
##==============================================================================
## end of 21 loops (jedirescale writes aout/aout*.fits)
##==============================================================================


# average the 21 fits files from aout/*.fits and write to
# out1/trial0_LSST_convolved.fits
run_process("jediaverage",['./executables/jediaverage',
    config['output_file'],
    config['LSST_convolved_image']])




# simulate exposure time and add Poisson noise
run_process("jedinoise", ['./executables/jedinoise',
    config['LSST_convolved_image'],
    config['exp_time'],
    config['noise_mean'],
    config['LSST_convolved_noise_image']])




# modified aug 3, 2016
# add noise to aout/aout10.fits and choose this as monochromatic psf
run_process("jedinoise", ['./executables/jedinoise',
    'aout/aout10.fits',
    config['exp_time'],
    config['noise_mean'],
    'aout/aout10_noise.fits'])
















## *****************************************************************************
##==============================================================================
## 90 degree rotated case needs catalogs from non rotated outputs
##==============================================================================
## *****************************************************************************


pre = "90_"
config_record['90_prefix']              = pre + config_record['prefix']
config_record['90_output_folder']       = pre+config_record['output_folder']
config['90_output_folder']              = config_record['90_output_folder']




# make 90_out1/90_key things for 90 degree rotated case
for i in range(len(keys)):
    key = keys[i]
    config['90_' + key] = config_record['90_output_folder'] + config_record['90_prefix'] + config_record[key]
    string = '90_' + key
    print(string,' = ', config[string])






# create output folder
if (not os.path.exists(config['90_output_folder'])):
    os.makedirs(config['90_output_folder'])




# create folder for convolved images
convolved_path = "%sconvolved/"%(config['90_output_folder'])
if not os.path.exists(convolved_path):
    os.makedirs(convolved_path)


# create stamps and distorted folders
for x in range(0, int(math.ceil(float(config['num_galaxies'])/1000))):
    postage_path = "%sstamp_%i"%(config['90_output_folder'],x)
    distorted_path = "%sdistorted_%i"%(config['90_output_folder'],x)
    if not os.path.exists(postage_path): os.makedirs(postage_path)
    if not os.path.exists(distorted_path): os.makedirs(distorted_path)


# read old catalog file and rotate angle
old_catalog_file= open(config['catalog_file'], 'r')
catalog_file= open(config['90_catalog_file'], 'w')
for old_line in old_catalog_file:
    l = old_line.split("\t")
    angle = float(l[3])+90
    angle -= 360*(int(angle)/360)
    l[3] = str(angle)
    l[-1]= l[-1].replace(config['output_folder'],config['90_output_folder'])
    l[-2]= l[-2].replace(config['output_folder'],config['90_output_folder'])
    line = "\t".join(l)
    catalog_file.write(line)
old_catalog_file.close()
catalog_file.close()




# create new convolved list from old list
old_convolvedlist_file= open(config['convolvedlist_file'], 'r')
convolvedlist_file= open(config['90_convolvedlist_file'], 'w')
for old_line in old_convolvedlist_file:
    line = old_line.replace(config['output_folder'],config['90_output_folder'])
    convolvedlist_file.write(line)
old_convolvedlist_file.close()
convolvedlist_file.close()



# create new distorted list from old list
old_distortedlist_file = open(config['distortedlist_file'], 'r')
distortedlist_file     = open(config['90_distortedlist_file'], 'w')

for old_line in old_distortedlist_file:
    line = old_line.replace(config['output_folder'],config['90_output_folder'])
    distortedlist_file.write(line)

old_distortedlist_file.close()
distortedlist_file.close()





# create list of psf and outfile for 90 degree rotated case
psf90,outfile90     = [],[]

# psf90 file, same as psf file
with open(config['psf_file'],"r")       as f: psf90     = f.readlines()
with open(config['90_output_file'],"r") as f: outfile90 = f.readlines()

# print the list
for i in range(len(psf90))    : print(psf90[i],end='')
for i in range(len(outfile90)): print(outfile90[i],end='')



## run jedicolor.c, creates 101 fitsfiles inside simdatabase/f1/
run_process("jedicolor",['./executables/jedicolor',
    "physics_settings/color.txt",
    str(1.0) ])





##==============================================================================
## 21 loop for 90 rotated case
##==============================================================================

for j in range(0,21):

    # jedicolor creates 101 fitsfiles inside simdatabase/f1/
    run_process("jedicolor",['./executables/jedicolor',
    "physics_settings/color.txt",
    str(j/20.0) ])

    # make postage stamp images that fit the catalog parameters
    run_process("jeditransform", ['./executables/jeditransform',
      config['90_catalog_file'],
      config['90_dislist_file']])

    # lens the galaxies one at a time
    run_process("jedidistort", ['./executables/jedidistort',
      config['nx'],
      config['ny'],
      config['90_dislist_file'],
      config['lenses_file'],
      config['pix_scale'],
      config['lens_z']])

    # combine the lensed galaxies onto one large image
    run_process("jedipaste", ['./executables/jedipaste',
      config['nx'],
      config['ny'],
      config['90_distortedlist_file'],
      config['90_HST_image']])

    # convonlve the large image with the PSF
    # this creates one image for each band of the image
    run_process("jediconvolve", ['./executables/jediconvolve',
      config['90_HST_image'],
      psf90[j],
      convolved_path])

    # combine each band into a single image
    run_process("jedipaste", ['./executables/jedipaste',
      config['nx'],
      config['ny'],
      config['90_convolvedlist_file'],
      config['90_HST_convolved_image']])

    # scale the image down from HST to LSST scale and trim the edges
    run_process("jedirescale", ['./executables/jedirescale',
      config['90_HST_convolved_image'],
      config['pix_scale'],
      config['final_pix_scale'],
      config['x_trim'],
      config['y_trim'],
      outfile90[j]])
##==============================================================================
## end of 21 loops for 90 rotated case
##==============================================================================


# average the aout/*.fits and get out1/trail0_LSST_convolved.fits
run_process("jediaverage",['./executables/jediaverage',
    config['90_output_file'],
    config['90_LSST_convolved_image']])

# simulate exposure time and add Poisson noise
# take in out1/trial0_LSST_convolved.fits add noise to it
# then, create out1/trial0_LSST_convolded_noise.fits
run_process("jedinoise", ['./executables/jedinoise',
    config['90_LSST_convolved_image'],
    config['exp_time'],
    config['noise_mean'],
    config['90_LSST_convolved_noise_image']])



# modified Aug 3, 2016
# add noise to aout/90_aout10.fits and choose this as monochromatic psf
run_process("jedinoise", ['./executables/jedinoise',
    r'aout/90_aout10.fits',
    config['exp_time'],
    config['noise_mean'],
    r'aout/90_aout10_noise.fits'])

# success
print("jedisim successful! Exiting.")

