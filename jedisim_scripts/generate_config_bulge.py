#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : Bhishan Poudel
# Date      : Jul 20, 2016


# Imports
from __future__ import print_function


# data
data = '''#---------------------physics settings-----------------------
pix_scale=0.03  		# pixel scale to use (arseconds per pixel)
final_pix_scale=0.2		# LSST pixscale (arcsecords per pixel)
exp_time=6000			# exposure time in seconds
noise_mean=10			# mean for poisson noise
nx=12288        		# number of pixels in the x direction
ny=12288        		# number of pixels in the y direction
x_border=301    		# must be large enough so that no image can overflow_
y_border=301    		# must be large enough so that no image can overflow
x_trim=480			    # larger than x_border to ensure no edge effects
y_trim=480			    # larger than y_border to ensure no edge effects
num_galaxies=12420		# number of galaxies to simulate 138,000 default
min_mag=22      		# minimum magnitude galaxy to simulate (inclusive)
max_mag=28      		# maximum magnitude galaxy to simulate (inclusive)
single_redshift=0		# use a single source galaxy redshift? 0 = no, 1=yes
fixed_redshift=1.5		# the single source galaxy redshift to use
power=0.33      		# power for the power law galaxy distribution
lens_z=0.3			    # the redshift of the lenses
#-------------------- lens and psf files -------------------------------------
lenses_file="physics_settings/lens.txt"	 # catalog of lenses to use
psf_file="physics_settings/psf.txt"      # the PSF to use
90_psf_file="physics_settings/psf.txt"   # the PSF to use
#-------------------------------output folders--------------------------------
output_folder="out1/"        # jedicatalog will create folders here
output_folder90="90_out1/"   # jedicatalog will create folders here
output_folder_avg="aout"     # jediaverage will write fits files here
output_folder_bulge="simdatabase/bulge_blue_red/" # jedicolor writes fitsfiles
output_folder_disk="simdatabase/disk_blue_red/"   # jedicolor writes fitsfiles
#-------------------------------output settings--------------------------------
prefix="trial0_"
sign="!"
HST_image="HST.fits"
HST_convolved_image="HST_convolved.fits"
LSST_convolved_image="LSST_convolved.fits"
LSST_convolved_noise_image="LSST_convolved_noise.fits"
output_file="physics_settings/out.txt"
90_output_file="physics_settings/90_out.txt"
#----------------------------database folders----------------------------------
#must contain files "n.txt" for n= min_mag to max_mag
radius_db_folder="simdatabase/radius_db/"
red_db_folder="simdatabase/red_db/"
#---------------------------catalog file locations-----------------------------
catalog_file="catalog.txt"
dislist_file="dislist.txt"
convlist_file="toconvolvelist.txt"
distortedlist_file="distortedlist.txt"
convolvedlist_file="convolvedlist.txt"
#------------------------additional input files--------------------------------
color_infile="physics_settings/bulge.txt"
#----------------------------source images-------------------------------------
num_source_images=101
# all postage stamp images should be on their own line, prefaced with image
# postage stamp images should be fits" file including the following header
# MAG      : magnitude of the postage stamp image
# MAG0     : magnitude zeropoint of the postage stamp image
# PIXSCALE : pixel scale of the postage stamp image
# RADIUS   : R50 radius of the image, in pixels
'''
# for disk and bulges 3 changes in this script.
config_path = r'physics_settings/bulge.conf'
with open(config_path, 'w') as f:
    f.write(data)


# add image names
num_source_images = 101
with open(config_path, 'a') as f:
    for i in range(num_source_images):
        line = r'image="simdatabase/bulge_blue_red/out{:d}.fits"'.format(i) + '\n'
        f.write(line)
