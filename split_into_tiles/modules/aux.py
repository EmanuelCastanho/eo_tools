#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
Auxiliar functions.

@author: Emanuel Castanho
"""

###############################################################################
# Import libraries
import os
import shutil

###############################################################################
def create_brand_new_folder(folder_name):
    """
    This function creates a folder if doesnt exist. If the folder exists, the function 
    deletes it and creates a new one.
    Input:  folder_name - Name of the folder to be created.
    Output: Brand new folder.
    """
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    else:
        shutil.rmtree(folder_name)
        os.mkdir(folder_name)

###############################################################################
def start_points(size, split_size, overlap=0):
    """
    From: https://github.com/Devyanshu/image-split-with-overlap
    """
    points = [0]
    stride = int(split_size * (1-overlap))
    counter = 1
    while True:
        pt = stride * counter
        if pt + split_size >= size:
            if split_size == size:
                break
            points.append(size - split_size)
            break
        else:
            points.append(pt)
        counter += 1
    return points

###############################################################################