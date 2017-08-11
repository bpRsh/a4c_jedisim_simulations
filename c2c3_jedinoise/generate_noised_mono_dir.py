#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
#
# Author    : Bhishan Poudel
# Date      : Sep 18, 2016

# Imports
from __future__ import print_function


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




outfolder = 'jedisim_out/noised_monochromatic'
replace_outfolder(outfolder)
