#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
Auxiliar functions.

@author: Emanuel Castanho
"""

############################################################################################
# Import libraries
import os
import shutil

############################################################################################
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

############################################################################################