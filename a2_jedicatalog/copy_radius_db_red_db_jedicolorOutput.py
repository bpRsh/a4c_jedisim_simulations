#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
# Author    : Bhishan Poudel
# Date      : Jul 20, 2016


# Imports
import os
import shutil
import errno

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

# copy radius database
src1 = '/Users/poudel/jedisim/simdatabase/radius_db'
dst1 = 'simdatabase/radius_db'
if not os.path.isdir(dst1):
    copyanything(src1, dst1)
    
 
# copy redshift database    
src2 = '/Users/poudel/jedisim/simdatabase/red_db'
dst2 = 'simdatabase/red_db'
if not os.path.isdir(dst2):
    copyanything(src2, dst2)


# copy bulge_disk_f8 folder created by jedicolor as input for jeditransform. 
src3 = '/Users/poudel/jedisim/simdatabase/bulge_disk_f8'
dst3 = 'simdatabase/bulge_disk_f8'
if not os.path.isdir(dst3):
    copyanything(src3, dst3)
