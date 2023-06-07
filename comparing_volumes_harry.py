# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 20:02:52 2023

@author: ingvieb
"""


############ USE OF ELASTIX TO TRANSFORM VOLUMES


#### NB: be aware that there is another package called simpleITK. to make sure you import the right package, 
# first use pip install SimpleITK-SimpleElastix

import SimpleITK as sitk
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

### DEFINE THE FILES TO WORK WITH

age = "P28"

working_path = "C:/Users/ingvieb/Elastix_testing/" + age + "//"

# give the paths of the volumes to be used as fixedImage and movingImage. in this case, the CCFvolume will be the moving and the DeMBA volume will be the fixed.
CCFVolume = working_path + "average_template_10_reoriented_FINAL.nii.gz" #"2023-04-04_LMR-registration_" + age + "_avg_nl.nii"
DeMBAVolume = working_path + age + "_reoriented_FINAL.nii"

# elastix read fixed and moving images
fixedImage = sitk.ReadImage(DeMBAVolume)
movingImage = sitk.ReadImage(CCFVolume)

# give the path of a segmentation volume, to be transformed according to the transform from fixedImage -> movingImage
movingSegmentation = working_path + "annotation_10_reoriented_FINAL.nii.gz" #"2023-04-04_LMR-registration_" + age + "_seg_nl.nii"

# set names for the resulting template and segmentation files

resultTemplateName = working_path + age + 'result_template_NEW.nii'
resultSegmentationName = working_path + age + "result_segmentation_NEW.nii"

# give the path of files with corresponding points in the fixedImage and movingImage. these will be considered during the registration
# fixedPoints = working_path + age + "_points.pts"
# movingPoints = working_path + "adult_points.pts"

fixed_numpy = sitk.GetArrayFromImage(fixedImage)
moving_numpy = sitk.GetArrayFromImage(movingImage)

resultslice = fixed_numpy[:,:,378]
plt.imshow(resultslice, cmap='magma', vmin=0, vmax=2500)
plt.show()

resultslice = moving_numpy[:,:,378]
plt.imshow(resultslice, cmap='magma', vmin=0, vmax=2500)
plt.show()