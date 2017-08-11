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

    for i in range(low,high):
        print('{} {} {}{}'.format('core_num = ',core_num, 'i = ', i))

    for j in range(13):
        print('{} {} {}{}'.format('core_num = ',core_num, 'j = ', j))


    for k in range(13):
        print('{} {} {}{}'.format('core_num = ',core_num, 'k = ', k))



# python3 test_par.py > junk.txt && open junk.txt then search i



# Running parallel
def func1(): jedisim_loop(low=0,high=5,core_num=0)
def func2(): jedisim_loop(low=5,high=10,core_num=1)
def func3(): jedisim_loop(low=10,high=15,core_num=2)
def func4(): jedisim_loop(low=15,high=21,core_num=3)
runInParallel(func1, func2,func3,func4)
