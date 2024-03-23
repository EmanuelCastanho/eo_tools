#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
"""
split_into_tiles
This function splits a TIF image into multiple tiles with a percentage of overlap.
The tiles are saved into a folder called results.

@author: Emanuel Castanho
"""
print("\nRunning split_into_tiles... \n")

# Environment
# conda create -n split_into_tiles-env python=3.10
# conda activate split_into_tiles-env
# conda install -c conda-forge gdal=3.8.4

# Import libraries
from osgeo import gdal
import numpy as np

# Import defined modules
from modules.aux import *

###############################################################################
# User inputs

# Path to TIF image to split.
# String
tif_path = "data/example.tiff"

# Tile size. Size of the tile in the format (width, height).
# Tuple
tile_size = (416, 416)

# Horizontal overlap between tiles from 0 to 0.99.
# Integer
overlap = 0

###############################################################################

# Create brand new folder to store the tiles
create_brand_new_folder("results")

# Open TIF
tif_open = gdal.Open(tif_path)
tif_data = tif_open.ReadAsArray()
tif_shape = tif_data.shape
tif_height = tif_shape[1]
tif_width = tif_shape[2]
print('')
print("Image to split: " + str(tif_width) + "x" + str(tif_height))

# Tile info
tile_width = tile_size[0]
tile_height = tile_size[1]
print("Desired tile: " + str(tile_width) + "x" + str(tile_height))

# Split points
assert 0 <= overlap < 1, "Invalid overlap."
x_points = start_points(tif_width, tile_width, overlap)
y_points = start_points(tif_height, tile_height, overlap)

# Split into tiles
row_count = 0
for y in y_points:
    column_count = 0
    for x in x_points:
        tile = tif_data[:, y:y+tile_height, x:x+tile_width] 
        tile_nbands = tile.shape[0]
        print("Processed tile: " + str(tile_nbands) + "," + str(tile.shape[2]) + "x" + str(tile.shape[1]))
        
        # Tile path
        tile_path = os.path.join("results", str(tile_width)+'x'+str(tile_height)+"_patch_"+str(row_count)+"-"+str(column_count)+".tif")

        # Init tile saving
        driver = gdal.GetDriverByName("GTiff")
        tile_data = driver.Create(tile_path, tile_width, tile_height, tile_nbands, gdal.GDT_Float32)
        
        # Set georeference for the tile
        geo_transform = list(tif_open.GetGeoTransform())
        geo_transform[0] = geo_transform[0] + x*geo_transform[1] + y*geo_transform[2]
        geo_transform[3] = geo_transform[3] + x*geo_transform[4] + y*geo_transform[5]
        tile_data.SetGeoTransform(tuple(geo_transform))    
        tile_data.SetProjection(tif_open.GetProjection())

        # Write tile data to give path
        for band in range(0, tile_nbands):             
            tile_data.GetRasterBand(band+1).WriteArray(tile[band, :, :])
            tile_data.GetRasterBand(band+1).SetNoDataValue(np.NaN)
        tile_data.FlushCache()
        tile_data = None
            
        column_count += 1
    row_count += 1

tif_open = None

