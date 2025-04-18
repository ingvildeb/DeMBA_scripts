# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 21:32:54 2024

@author: ingvieb
"""


import cv2
import numpy as np
import glob
from PIL import Image, ImageOps

import matplotlib.pyplot as plt


"""
This code makes videos out of ITK-snap screenshots.

"""


img_paths = [r"Z:\HBP_Atlasing\Developmental_atlases\DeMBA_Developmental mouse brain atlas\DeMBA-v1\01_working-environment\02_Figures\Videos\screenshot_itksnap\\",
             r"Z:\HBP_Atlasing\Developmental_atlases\DeMBA_Developmental mouse brain atlas\DeMBA-v1\01_working-environment\02_Figures\Videos\calb1_screenshots\\"]

img_types = ["template", "calb1"]

out_path = r"Z:\HBP_Atlasing\Developmental_atlases\DeMBA_Developmental mouse brain atlas\DeMBA-v1\01_working-environment\02_Figures\Videos\\"



def resize_with_padding(img, expected_size):
    img.thumbnail((expected_size[0], expected_size[1]))
    # print(img.size)
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (
        pad_width,
        pad_height,
        delta_width - pad_width,
        delta_height - pad_height,
    )
    return ImageOps.expand(img, padding)


# Pick dimensions for the final video.
size = 750, 750
views = ["Volumetric", "Horizontal", "Coronal", "Sagittal"]


for img_path, img_type in zip(img_paths, img_types):
    
    list_of_images = glob.glob(f"{img_path}*.png")
    
    for view in views:
        img_array = []
        list_of_ages = list(range(4, 57))
    
        for image, age in zip(list_of_images, list_of_ages):
            im = Image.open(image)
            
            # Setting the points for cropped image
            if view == "Volumetric":
                left = 400
                top = 730
                right = 1300
                bottom = 1300
            elif view == "Horizontal":
                left = 197
                top = 53
                right = 1344
                bottom = 690
            elif view == "Coronal":
                left = 1392
                top = 60
                right = 2520
                bottom = 689
            elif view == "Sagittal":
                left = 1380
                top = 729
                right = 2524
                bottom = 1358
    
            # Cropped the image and pad to selected dimensions
            im1 = im.crop((left, top, right, bottom))
            im1 = resize_with_padding(im1, (size))
            im1 = im1.crop((0, 100, 750, 750))
    
            # Append all images to array
            img_array.append(np.array(im1))
            
            # Save the image
            im1.save(f"{out_path}cropped_images\{img_type}\{view}\\P{age}_{img_type}_{view}.png")
            
    
        
        out = cv2.VideoWriter(
            f"{out_path}compiled_videos\\video_{img_type}_{view}.mp4", cv2.VideoWriter_fourcc(*"MP4V"), 4, im1.size
        )
    
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 500)
        org2 = (500, 500)
        fontScale = 1
        color = (255, 255, 255)  # BGR
        thickness = 2
    
        with_text = []
        for i, j in zip(img_array, list_of_ages):
            img_text = cv2.putText(
                i, f"Postnatal day {j}", org, font, fontScale, color, thickness, cv2.LINE_AA
            )
            img_text = cv2.putText(
                i, f"{view} view", org2, font, fontScale, color, thickness, cv2.LINE_AA
            )
            with_text.append(img_text)
    
        for i in img_array:
            out.write(cv2.cvtColor(i, cv2.COLOR_RGB2BGR))
    
        out.release()
