#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 20, 2016
# Last update :
#

# Imports




##==============================================================================
## Parallel programming
##==============================================================================
def runInParallel(*fns):

    # Imports
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
##==============================================================================
def jedisim_loop(low,high,core_num):
    """ Arguments:
        low,high = limits, eg. 0-5 or 5-10 or 10-15 or 15-21
        core_num = 0,1,2 or 3
    """

    for loop_num in range(low,high):

        # Depends: ~/jedisim/simdatabase/colors/*.fits
        #          jedisim_out/color_out/color0.txt
        #          jedisim_out/color_out/color_out0 will be replaced, not the color0.txt

        # Creates: jedisim_out/color_out/color_out0/blue_red_0_to100.fits as from color0.txt
        # jedicatalog and jeditransform need these fitsfiles
        print('{} {} {}{}'.format('core_num = ',core_num, 'loop_num = ', loop_num))




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
            print('{} {} {}{}'.format('core_num = ',core_num, 'j = ', j))






        # lens the galaxies one at a time
        # Depends     : 1. jedisim_out/out0/trial0_dislist.txt
        #               2. physics_settings/lens.txt
        #               3. jedisim_out/out0/stamp_0_to_12/stamp_0_to_999.fits.gz ( 12420 input zipped galaxies)
        #               4. jedisim_out/out0/distorted_0_to_12/  ( 13 empty folder to write unzipped distorted galaxies)
        #
        #
        # Creates     : 1. jedisim_out/out0/distorted_0_to_12/distorted_0_to_12419.fits
        for k in range(13):
            print('{} {} {}{}'.format('core_num = ',core_num, 'k = ', k))




# Running parallel
def func1(): jedisim_loop(low=0,high=5,core_num=0)
def func2(): jedisim_loop(low=5,high=10,core_num=1)
def func3(): jedisim_loop(low=10,high=15,core_num=2)
def func4(): jedisim_loop(low=15,high=21,core_num=3)
runInParallel(func1, func2,func3,func4)
