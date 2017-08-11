#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
#
# Date        : Jul 8, 2013
# Last update : Sep 17, 2016
#
# Estimated time:

# Imports
from __future__ import print_function


def generate_color_txt():

    #imports
    import os

    for i in range(4):


        num_galaxies = 101
        outfolder = 'jedisim_out/color_out/color_out{:d}'.format(i)
        if not os.path.exists(outfolder): os.makedirs(outfolder)


        outfile = "physics_settings/color{:d}.txt".format(i)
        with open (outfile, 'w') as fout:
            for j in range(101):
                blue = 'simdatabase/colors/f606w_gal{:-d}.fits'.format(j)
                red  = 'simdatabase/colors/f814w_gal{:-d}.fits'.format(j)


                out  = outfolder + '/blue_red_{:-d}.fits'.format(j)
                line = blue + '  ' + red + '  ' + out
                print(line,file=fout)


        print('{} {} {}'.format('output file : ',outfile, ''))

if __name__ == '__main__':

    generate_color_txt()
