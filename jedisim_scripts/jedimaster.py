#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Bhishan Poudel <poudel>
# @Date:   06-Sep-2016 17:09
# @Last modified by:   poudel
# @Last modified time: 18-Nov-2016 17:11
#
# Inputs      : 1. executables/*
#                      1.jedicolor 2.jedicatalog 3.jedicolor 4.jeditransform
#                      5.jedidistort 6.jedipaste 7.jediconvolve 8.jedipaste
#                      9.jedirescale 10.jediaverage 11.jedinoise 12.jedinoise
#
#               2. physics_settings/*
#                   config1.conf psf.txt lens.txt color.txt out.txt 90_out.txt
#
#               3. psf/*
#                   psf0.fits ... psf20.fits
#
#               4. simdatabase/*
#                   colors/f606w_gal0.fits f814w_gal0.fits (202 fitsfiles)
#                   f1 (empty folder, jedicolor will create fitsfiles out.fits)
#                   radius_db/20.dat to 29.dat
#                   red_db/19.dat to 33.dat and 99.dat and -99.dat
#
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
#    This prgoram takes in 101 blue galaxies
#    ( simdatabase/colors/f606w_gal*.fits)
#                     101 red galaxies( simdatabase/colors/f814w_gal*.fits)
#            and then, pix3[ii] = ((1-m)*pix1[ii])+(m*pix2[ii]); with m = 1.
#
#            This creates 101 galaxies inside simdatabase/f1/out*.fits
#
# 2. jedicatalog
# This program takes in : config1.conf,lens.txt,psf.txt, config_ouptput_folder,
#                         simdatabase/radius_db, simdatabase/red_db,
#                         simdatabase/f1/*.fits
#
#    And, creates       : config_output_folder/trial0_catalog.txt,
#                         config_output_folder/trial0_convolvedlist.txt
#                         config_output_folder/trial0_distortedlist.txt
# 3. jedicolor
#     Inside the loop this program does:
#       'jedicolor',  "physics_settings/color.txt",str(i/20.0)]
#
# 4. jeditransform
#       jeditransform, config['catalog_file'],config['dislist_file']])
#
# Estimated time : 6 hours for bulge.conf in MacOS.
# Command        : python3 jedimaster.py physics_settings/bulge.conf

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
program_start_time = time.time()
program_begin_time = time.ctime()


def replace_outfolder(outfolder):
    """Replace given directory."""
    # imports
    import shutil
    import os

    if os.path.exists(outfolder):
        print('Replacing folder: ', outfolder)
        shutil.rmtree(outfolder)
        os.makedirs(outfolder)
    else:
        print('Making new folder: ', outfolder)
        os.makedirs(outfolder)


def config_dict(config_path):
    """Create a dictionary of variables from input file."""
    # imports
    import re

    # parse config file and make a dictionary
    with open(config_path, 'r') as f:
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


def run_process(name, args,):
    """Run a process.

    Usage: run_process("example ", ["python ", 'example.py', 'arg1' ]) .
    """
    # imports
    import subprocess
    import sys

    print("\n\n\n", "#" * 40)
    print("# Description : %s\n# Commands :" % name, end=' ')
    for arg in args:
        print(arg, end=' ')

    print("\n", "#" * 39, end='\n\n')

    process = subprocess.Popen(args)

    process.communicate()
    if process.returncode != 0:
        print("Error: %s did not terminate correctly. \
              Return code: %i." % (name, process.returncode))
        sys.exit(1)
    else:
        print("\n\n", "#" * 39, end='\n')
        print("# Success! : %s " % name)
        print("#" * 40, "\n\n\n")


# create config dictionary
config_path = 'physics_settings/bulge.conf'
config = config_dict(config_path)

# print config dictionary
for key, value in config.items():
    print (key, value)

# make copy
config_record = copy.deepcopy(config)


# ==============================================================================
# make the filenames from the config parameters
# ==============================================================================
print(config['HST_image'])  # HST.fits
prefix = config['output_folder'] + config['prefix']  #


keys = ['HST_image',            'HST_convolved_image',
        'LSST_convolved_image', 'LSST_convolved_noise_image',
        'catalog_file',         'dislist_file',
        'distortedlist_file',   'convolvedlist_file']


for i in range(len(keys)):
    key = keys[i]
    config[key] = prefix + config[key]

print(config['HST_image'])  # jedisim_out/out0/trial0_HST.fits

# list of psf and outfiles
psf, outfile = [], []

# store lines to list
with open(config['psf_file'], "r") as f:
    psf = f.readlines()
with open(config['output_file'], "r") as f:
    outfile = f.readlines()

# print the list
# for i in range(len(psf)):
#     print(psf[i], end='')
# for i in range(len(outfile)):
#     print(outfile[i], end='')


# replace old output folders before running new simulation
outfolders = [config["output_folder"],
              config["output_folder90"],
              config["output_folder_avg"],
              config["output_folder_bulge"],
              config["output_folder_disk"]
              ]
for outfolder in outfolders:
    replace_outfolder(outfolder)


# create nencessary folders
# ======================================================================
if (not os.path.exists(config['output_folder'])):
    os.makedirs(config['output_folder'])


# make folder for convolved images
convolved_path = "%sconvolved/" % config['output_folder']
if not os.path.exists(convolved_path):
    os.makedirs(convolved_path)

# make folder for distorted images
for x in range(0, int(math.ceil(float(config['num_galaxies']) / 1000))):
    postage_path = "%sstamp_%i" % (config['output_folder'], x)
    distorted_path = "%sdistorted_%i" % (config['output_folder'], x)
    if not os.path.exists(postage_path):
        os.makedirs(postage_path)
    if not os.path.exists(distorted_path):
        os.makedirs(distorted_path)

# =============================================================
# jedicolor creates 101 fitsfiles inside config['output_folder_bulge']
# jedicatalog needs this
run_process("jedicolor", ['./executables/jedicolor',
                          config['color_infile'],
                          str(1.0)])

# make the catalog of galaxies
run_process("jedicatalog", ["./executables/jedicatalog",
                            config_path])


# =============================================================
# =============================================================
for i in range(0, 21):

    # jedicolor creates 101 fitsfiles inside config['output_folder_bulge']
    run_process("jedicolor", ['./executables/jedicolor',
                              config['color_infile'],
                              str(i / 20.0)])

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
# ==============================================================
# ==============================================================


# average the 21 fits files from aout/*.fits and write to
# out1/trial0_LSST_convolved.fits
run_process("jediaverage", ['./executables/jediaverage',
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
                          r'aout/aout10.fits',
                          config['exp_time'],
                          config['noise_mean'],
                          r'aout/aout10_noise.fits'])


# ============================================================
# ============================================================
# ============================================================
# make the folder for the 90_ simulations

pre = "90_"
config_record['90_prefix'] = pre + config_record['prefix']
config_record['90_output_folder'] = pre + config_record['output_folder']
config['90_output_folder'] = config_record['90_output_folder']

config['90_HST_image']                  = config_record['90_output_folder'] + \
    config_record['90_prefix'] + \
    config_record['HST_image']
config['90_HST_convolved_image']        = config_record['90_output_folder'] + \
    config_record['90_prefix'] + \
    config_record['HST_convolved_image']
config['90_LSST_convolved_image']       = config_record['90_output_folder'] + \
    config_record['90_prefix'] + \
    config_record['LSST_convolved_image']
config['90_LSST_convolved_noise_image'] = config_record['90_output_folder'] + \
    config_record['90_prefix'] + \
    config_record['LSST_convolved_noise_image']
config['90_catalog_file']               = config_record['90_output_folder'] + \
    config_record['90_prefix'] + \
    config_record['catalog_file']
config['90_dislist_file']               = config_record['90_output_folder'] + \
    config_record['90_prefix'] + \
    config_record['dislist_file']
config['90_distortedlist_file']         = config_record['90_output_folder'] + \
    config_record['90_prefix'] + \
    config_record['distortedlist_file']
config['90_convolvedlist_file']         = config_record['90_output_folder'] + \
    config_record['90_prefix'] + \
    config_record['convolvedlist_file']

print(config_record['90_prefix'])
print(config_record['90_output_folder'])
print(config['90_HST_image'])
print(config['90_HST_convolved_image'])
print(config['90_LSST_convolved_image'])
print(config['90_LSST_convolved_noise_image'])
print(config['90_catalog_file'])
print(config['90_dislist_file'])
print(config['90_distortedlist_file'])
print(config['90_convolvedlist_file'])


# =============================================================
# if the output folder doesn't exist, create it
if (not os.path.exists(config['90_output_folder'])):
    os.makedirs(config['90_output_folder'])


# =============================================================
# make folder for convolved images
convolved_path = "%sconvolved/" % (config['90_output_folder'])
if not os.path.exists(convolved_path):
    os.makedirs(convolved_path)


# =============================================================
# make folders because cfitsio is bad at it
for x in range(0, int(math.ceil(float(config['num_galaxies']) / 1000))):
    postage_path = "%sstamp_%i" % (config['90_output_folder'], x)
    distorted_path = "%sdistorted_%i" % (config['90_output_folder'], x)
    if not os.path.exists(postage_path):
        os.makedirs(postage_path)
    if not os.path.exists(distorted_path):
        os.makedirs(distorted_path)


# ==============================================================
old_catalog_file = open(config['catalog_file'], 'r')
catalog_file = open(config['90_catalog_file'], 'w')
for old_line in old_catalog_file:
    l = old_line.split("\t")
    angle = float(l[3]) + 90
    angle -= 360 * (int(angle) / 360)
    l[3] = str(angle)
    l[-1] = l[-1].replace(config['output_folder'], config['90_output_folder'])
    l[-2] = l[-2].replace(config['output_folder'], config['90_output_folder'])
    line = "\t".join(l)
    catalog_file.write(line)
old_catalog_file.close()
catalog_file.close()


# =============================================================
old_convolvedlist_file = open(config['convolvedlist_file'], 'r')
convolvedlist_file = open(config['90_convolvedlist_file'], 'w')
for old_line in old_convolvedlist_file:
    line = old_line.replace(config['output_folder'],
                            config['90_output_folder'])
    convolvedlist_file.write(line)
old_convolvedlist_file.close()
convolvedlist_file.close()


# ===============================================================
old_distortedlist_file = open(config['distortedlist_file'], 'r')
distortedlist_file = open(config['90_distortedlist_file'], 'w')
for old_line in old_distortedlist_file:
    line = old_line.replace(config['output_folder'],
                            config['90_output_folder'])
    distortedlist_file.write(line)
old_distortedlist_file.close()
distortedlist_file.close()


# =============================================================
# list of psf and outfile for 90 degree rotated case
psf90, outfile90 = [], []

# psf90 file, same as psf file
with open(config['psf_file'], "r") as f:
    psf90 = f.readlines()
with open(config['90_output_file'], "r") as f:
    outfile90 = f.readlines()

# print the list
for i in range(len(psf90)):
    print(psf90[i], end='')
for i in range(len(outfile90)):
    print(outfile90[i], end='')

# ================================================================
# run jedicolor.c, creates 101 fitsfiles inside config['output_folder_bulge']
run_process("jedicolor", ['./executables/jedicolor',
                          config['color_infile'],
                          str(1.0)])


# ================================================================
# ================================================================
for j in range(0, 21):

    # jedicolor creates 101 fitsfiles inside config['output_folder_bulge']
    run_process("jedicolor", ['./executables/jedicolor',
                              config['color_infile'],
                              str(j / 20.0)])

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
# =================================================================
# =================================================================


# average the aout/*.fits and get out1/trail0_LSST_convolved.fits
run_process("jediaverage", ['./executables/jediaverage',
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


# modified aug 3, 2016
# add noise to aout/90_aout10.fits and choose this as monochromatic psf
run_process("jedinoise", ['./executables/jedinoise',
                          r'aout/90_aout10.fits',
                          config['exp_time'],
                          config['noise_mean'],
                          r'aout/90_aout10_noise.fits'])

# success
print("jedisim successful! Exiting.")


# print the time taken
program_end_time = time.time()
seconds = program_end_time - program_start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)
print('\nProgram started at : ', program_begin_time)
print('\nProgram ended at   : ', time.ctime())
print("\nTime taken to run whole program ==> {:2.0f} days, {:2.0f} hours,\
        {:2.0f} minutes, {:f} seconds.".format(d, h, m, s))
