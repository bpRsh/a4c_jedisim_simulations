#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Aug 15, 2016
# Last update : 
#
# Inputs      : psf/psf*.fits
#               
# Outputs     : weighted_psf.fits
#               
# Info:
# 1. This program creates weighted average of the input fitsfiles.
#    Algorithm: output = data_i * weight_i / sum(weight)
#
# 2. The weight range 1 to 1.2 are the average flux ratio of 100 f606 and f814
#    galaxies. (refer: ~/jedisim/simdatabase/average_flux_ratio.py)
#
# Estimated time: 3 sec
# 

# Imports
from astropy.io import fits
import numpy as np
import time



def weighted_psf(indir):
    '''
# Depends :
#
# Outputs :
#
# Returns :
#
# Info:
# 1.
#
    '''

    # weights
    # range 1 to 1.2 are the average flux ratio of 100 f606 and f814 galaxies
    # (refer: ~/phosim/simdatabase/average_flux_ratio.py)
    nfiles = 21
    weight = np.linspace(1.0,1.2,num=nfiles,endpoint=True)
    
    # read data from first input file
    dat = fits.getdata(indir+'/psf0.fits')
    
    # make data all zero
    dat = dat * 0.0
    
    # average the data
    for i in range(0,nfiles):
        infile = indir + '/psf{:d}.fits'.format(i)
        tmp    = fits.getdata(infile) * weight[i]
            
        # add data
        dat += tmp    
        
        if i ==(nfiles-1):
            dat = dat/sum(weight)
    
    # create HDU objects to write fitsfiles
    hdu      = fits.PrimaryHDU()
    hdu.data = dat
    
    
    # write to a fitsfile
    outfile = 'weighted_psf.fits'
    hdu.writeto(outfile, clobber=True)
    
    # output info
    print('{} {} {}'.format('\nCreating file: ',outfile, ''))




##==============================================================================
## Main program
##==============================================================================
if __name__ == '__main__':

    # beginning time
    begin_time,begin_ctime = time.time(), time.ctime()

    # run main program
    weighted_psf('psf')

    # print the time taken
    end_time,end_ctime  = time.time(), time.ctime()
    seconds             = end_time - begin_time
    m, s                = divmod(seconds, 60)
    h, m                = divmod(m, 60)
    d, h                = divmod(h, 24)
    print('\nBegin time: ', begin_ctime,'\nEnd   time: ', end_ctime,'\n' )
    print("Time taken: {0:.0f} days, {1:.0f} hours, \
          {2:.0f} minutes, {3:f} seconds.".format(d, h, m, s))



