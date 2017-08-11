#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
# Author    : Bhishan Poudel
# Date      : Jul 20, 2016


# Imports
from __future__ import print_function


# data
data = '''# config file for jedimaster.py and associated programs
# a1.jedicolor    a2.jedicatalog
# b1.jedicolor    b2.jeditransform b3.jedidistort b4.jedipaste
# b5.jediconvolve b6.jedipaste     b7.jedirescale
# c1.jediaverage  c2.jedinoise     c3.jedinoise_10
#---------------------jedicolor------------------------------
# jedicolor will create simdatabase/f8_bulge_disk/f8_bulge_disk0.fits
# using input text files, i.e. scales bulge_f814w and disk_f818w galaxies
# jedicatalog will read MAG,MAG0,PIXSCALE,RADIUS from these files and
# will create three catalogs: out1/trial0_catalog.txt,convolved,distortedlist
color_infile="physics_settings/color.txt"
color_outfolder="simdatabase/f8_bulge_disk"
# jedicatalog will read these physics settings.
#---------------------physics settings-----------------------
nx=12288        		# x pixels            (arg for jedidistort)
ny=12288        		# y pixels            (arg for jedidistort)
pix_scale=0.03  		# arseconds per pixel (arg for jedidistort)
lens_z=0.3			    # lens redshift       (arg for jedidistort)
single_redshift=1		# 0 = not-fixed, 1=fixed
fixed_redshift=1.5		# the single source galaxy redshift to use
final_pix_scale=0.2		# LSST pixscale (arcsecords per pixel)
exp_time=6000			# exposure time in seconds
noise_mean=10			# mean for poisson noise
x_border=301    		# must be large enough so that no image can overflow_
y_border=301    		# must be large enough so that no image can overflow
x_trim=480			    # larger than x_border to ensure no edge effects
y_trim=480			    # larger than y_border to ensure no edge effects
num_galaxies=12420		# number of galaxies to simulate 138,000 default
min_mag=22      		# minimum magnitude galaxy to simulate (inclusive)
max_mag=28      		# maximum magnitude galaxy to simulate (inclusive)
power=0.33      		# power for the power law galaxy distribution
#--------------------psf and lenses--------------------------
# lens.txt has a single line with 5 parameters
# 6144 6144 1 1000.000000 4.000000
#  x    y  type p1       p2
#  x - x center of lens (in pixels)
#  y - y center of lens (in pixels)
#  type - type of mass profile
#         1. Singular isothermal sphere
#         2. Navarro-Frenk-White profile
#	       3. NFW constant distortion profile for grid simulations
#  p1 - first profile parameter
#         1. sigma_v [km/s]
#         2. M200 parameter [10^14 solar masses]
#		  3. Distance to center in px. M200 fixed at 20 default, which can be modified in case 3
#  p2 - second profile parameter
#         1. not applicable, can take any numerical
#         2. c parameter [unitless]
#         3. c parameter [unitless]
lenses_file="physics_settings/lens.txt"	  # arg for jedidistort
psf_file="physics_settings/psf.txt"       # psf for
90_psf_file="physics_settings/psf.txt"    # psf for
#--------------------output settings--------------------------
output_folder="out1/"  # jedicatalog etc.
prefix="trial0_"       # jedicatalog etc.
sign="!"               # jedicolor
HST_image="HST.fits"
HST_convolved_image="HST_convolved.fits"
LSST_convolved_image="LSST_convolved.fits"
LSST_convolved_noise_image="LSST_convolved_noise.fits"
output_file="physics_settings/out.txt"
90_output_file="physics_settings/90_out.txt"
#-----------database folders----------------------------------
# There are 10 radius database files 20.dat to 29.dat.
# which contains min and max radius to be used by jedicatalog.
# e.g. the file simdatabase/radius_db/20.dat has two lines: 36.72 3.51
# This must contain files "n.txt" for n= min_mag to max_mag
radius_db_folder="simdatabase/radius_db/"
# There are 15+2 redshift database files 19.dat to 33.dat with +- 99.dat.
# which contains min and max redshift to be used by jedicatalog.
# e.g. the file simdatabase/red_db/19.dat has two lines: 0.301000 0.138000
red_db_folder="simdatabase/red_db/"
#-----------catalog files for jedicatalog -----------------------------
# jedicatalog will write:
# name,x,y,angle,redshift,pixscale,old_mag,old_rad,new_mag,new_rad,stamp_name,dis_name
# in the out1/trial0_catalog.txt
# jedicatalog also creates out1/trial0_convolvedlist.txt
# which has 6 lines like: out1/convolved/convolved_band_0.fits
# jedicatalog also creates out1/trial0_distortedlist.txt
# it has 0-12 folders and 1000 fitsfiles (total: 12420 files)
# line     1: out1/distorted_0/distorted_0.fits
# line 12420: out1/distorted_12/distorted_12419.fits
catalog_file="catalog.txt"
convolvedlist_file="convolvedlist.txt"
distortedlist_file="distortedlist.txt"
#-----------catalog files for jedidistort -----------------------------
# jeditransform creates out1/trial0_dislist.txt along with 12420 .gz stamps
# jedidistort will use these files.
# Input galaxy parameter file for jedidistort: x y nx ny zs file
#           x - x coord. of lower left pixel where galaxy should be embedded
#           y - y coord. of lower left pixel where galaxy should be embedded
#           nx - width of the galaxy in pixels
#           ny - height of the galaxy in pixels
#           zs - redshift of this galaxy
#           infile - filepath to the FITS file for this galaxy, 1024 chars max
#           outfile - filepath for the output FITS file for this galaxy, 1024 chars max
#
#  e.g. out1/trial0_dislist.txt looks like this: (was created by jeditransform)
# 6813 888 10 23 1.500000 out1/stamp_0/stamp_.fits.gz out1/distorted_0/distorted_0.fits
# x    y   nx ny zs       infile                      outfile
dislist_file="dislist.txt"  # arg for jedidistort
convlist_file="toconvolvelist.txt"
#-----------source images-------------------------------------
num_source_images=302
# jedicolor scales bulge_f814w and disk_f814w galaxies and writes these files.
# jedicatalog will read MAG, MAG0, PIXSCALE, RADIUS from these files.
# jedicatalog will write these names in out1/trial0_catalog.txt
# Required headers:
# MAG      : magnitude of the postage stamp image
# MAG0     : magnitude zeropoint of the postage stamp image
# PIXSCALE : pixel scale of the postage stamp image
# RADIUS   : R50 radius of the image, in pixels
'''


num_source_images = 302
config_path = 'physics_settings/config.sh'
print('Creating: ', config_path)
with open(config_path, 'w') as f:
    f.write(data)


# add image names
with open(config_path, 'a') as f:
    for i in range(num_source_images):
        line = r'image="simdatabase/bulge_disk_f8/f8_bulge_disk{:d}.fits"'.format(i) + '\n'
        f.write(line)
