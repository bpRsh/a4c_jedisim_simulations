#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author    : Bhishan Poudel
# Date      : Jul 26, 2016
# Updated   : Sep 19, 2016

# Imports
from __future__ import print_function

num_outfiles = 21
for count in range(4):

    outfile   = "physics_settings/rescaled_convolved_lsst_out{:d}.txt".format(count)
    with open (outfile, 'w') as f:

        print('Creating: ', outfile)
        for i in range(num_outfiles):
            print('jedisim_out/rescaled_convolved_lsst_out{:d}/rescaled_convolved_lsst_{:-d}.fits'.format(count,i),file=f)



# note: 90 degree rotated outfile are created in jedimaster.py reading old outfile and rotating the angle
# e.g. rescaled_convolved_lsst_90_out0.txt

## read old catalog file and rotate angle
#old_catalog_file= open('physics_settings/rescaled_convolved_lsst_out0.txt', 'r')
#catalog_file= open('physics_settings/rescaled_convolved_lsst_90_out0.txt', 'w')
#for old_line in old_catalog_file:
    #l = old_line.split("\t")
    #angle = float(l[3])+90
    #angle -= 360*(int(angle)/360)
    #l[3] = str(angle)
    #l[-1]= l[-1].replace(config['output_folder'],config['90_output_folder'])
    #l[-2]= l[-2].replace(config['output_folder'],config['90_output_folder'])
    #line = "\t".join(l)
    #catalog_file.write(line)
#old_catalog_file.close()
#catalog_file.close()
