#!/usr/local/bin/env python
# -*- coding: utf-8 -*-
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Aug 03, 2016
# Last update : Sep 17, 2016



def replace_stamps():

    import os,shutil

    for i in range(13):

        outfolder = 'out1/stamp_{:d}'.format(i)
        if os.path.exists(outfolder):
            print('Replacing: ', outfolder)
            shutil.rmtree(outfolder)
            os.makedirs(outfolder)
        else:
             os.makedirs(outfolder)
             print('Creating: ', outfolder)


    # also delete dislist file
    out_dislist = 'out1/trial0_dislist.txt'
    if os.path.exists(out_dislist):
        print('Removing: ', out_dislist)
        os.remove(out_dislist)



if __name__ == '__main__':
    replace_stamps()

