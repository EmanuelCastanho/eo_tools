#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
shp_to_dic
This script converts each shapefile 2D polygon into a dictionary with coordenates that is 
saved inside a text file.
Used as auxiliar tool for POS2IDON pipeline and other projects.

@author: Emanuel Castanho
"""
print("\nRunning shp_to_dic... \n")

############################################################################################
# Environment setup:
# conda create -n shp_to_dic-env python=3.9
# conda activate shp_to_dic-env
# pip install pyshp==2.3.1

# Import libraries
import glob
import os
import shapefile # pyshp==2.3.1
import json
from modules.aux import create_brand_new_folder

############################################################################################
# User inputs

# Input folder with shapefile folders to convert
# String
input_shps_folder = "input_shapefiles"

# Output folder where the text files will be saved
# String
output_dics_folder = "output_dictionaries"

############################################################################################
# Check existing shapefiles
shps_list = glob.glob(os.path.join(input_shps_folder, "*"))

if len(shps_list) != 0:
    # Create brand new folder to save results
    create_brand_new_folder(output_dics_folder)

    # Cycle each shapefile
    for shp_folder_path in shps_list:
        shp_folder_name = os.path.basename(shp_folder_path)
        print("Converting " + shp_folder_name + " ...")
        # Read shapefile
        shp_file_path = glob.glob(os.path.join(shp_folder_path, "*.shp"))[0]
        shp = shapefile.Reader(shp_file_path)
        # Get the shapes
        shp_shapes = shp.shapes()
        # Extract coordinates and type
        shp_dict = {}
        for i, shape in enumerate(shp_shapes):
            print("Assuming " + str(shape) + " as Polygon type.")
            coords = shape.points
            shp_dict[i] = {"type": "Polygon",
                           "coordinates": [[list(coord) for coord in coords]]}
        # Convert the dictionary to a json and save inside text file
        with open(os.path.join(output_dics_folder, shp_folder_name+".txt"), 'w') as f:
            json.dump(list(shp_dict.values()), f)
        print("Dictionary with coordinates of shapefile saved inside text file.")
        print("")

else:
    print("No shapefiles to convert\n")

print("End of script.\n")

