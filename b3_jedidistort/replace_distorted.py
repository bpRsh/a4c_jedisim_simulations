#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Aug 03, 2016
# Last update : Sep 17, 2016

import os,shutil,errno

def replace_distorted():

    

    for i in range(13):

        outfolder = 'out1/distorted_{:d}'.format(i)
        if os.path.exists(outfolder):
            print('Replacing: ', outfolder)
            shutil.rmtree(outfolder)
            os.makedirs(outfolder)
        else:
             os.makedirs(outfolder)
             print('Creating: ', outfolder)

# replace old distorted folders
replace_distorted()

