# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:27:23 2023

@author: ingvieb
"""

from glob import glob
import shutil
import os
import datetime
import DeMBA_functions as dfs

path = r"C:\Users\ingvieb\elastix_testing//"
# give the paths of the volumes to be used as fixedImage and movingImage. in this case, the CCFvolume will be the moving and the DeMBA volume will be the fixed.

movingImage = f"{path}/average_template_10_adjusted_micronXYZT.nii.gz"
movingSegmentation = f"{path}/annotation_10_adjusted_micronXYZT.nii.gz"
fixedImage = f"{path}/P28_DeMBA_template_micronXYZT.nii.gz"
fixedPoints = f"{path}/p28_Thal_SC_points.pts"
movingPoints = f"{path}/adult_Thal_SC_points.pts"


runsdir = fr"{path}/runs/"
numberofruns = len(glob(fr"{runsdir}/*"))
fullrunsdir = fr"{runsdir}run{numberofruns}/"
os.mkdir(fullrunsdir)

resultTemplateName = f"{fullrunsdir}/resultTemplate.nii"
resultSegmentationName = f"{fullrunsdir}/resultSegmentation.nii"
deformationName = f"{fullrunsdir}/deformationField.nii"

# add th4 time stamp 
time = datetime.datetime.now()
# format time stamp
time = time.strftime("%d-%m-%Y %H:%M:%S")

# format
message = f"""
{time} \n
This is my first test. \n
bla bla bla. 

"""
# write to file
with open(f"{fullrunsdir}notes.txt", "w") as f:
    f.write(message)
    


dfs.runTransform(fixedImage, movingImage, fixedPoints, movingPoints, movingSegmentation, resultTemplateName, resultSegmentationName, deformationName)

    
shutil.copy(fixedPoints, f"{fullrunsdir}fixed.pts")
shutil.copy(movingPoints, f"{fullrunsdir}moving.pts")
shutil.copy("elastix.log", f"{fullrunsdir}elastix.log")
shutil.copy("TransformParameters.0.txt", f"{fullrunsdir}TransformParameters.0.txt")
shutil.copy("TransformParameters.1.txt", f"{fullrunsdir}TransformParameters.1.txt")
shutil.copy("TransformParameters.2.txt", f"{fullrunsdir}TransformParameters.2.txt")
shutil.copy("parameter_jsons/param_dict_t.json", f"{fullrunsdir}param_dict_t.json")
shutil.copy("parameter_jsons/param_dict_a.json", f"{fullrunsdir}param_dict_a.json")
shutil.copy("parameter_jsons/param_dict_b.json", f"{fullrunsdir}param_dict_b.json")
shutil.copy("deform_niss_with_points.py", f"{fullrunsdir}script.py")

# shutil.copy(movingImage, f"{fullrunsdir}movingImage.nii")
# shutil.copy(fixedImage, f"{fullrunsdir}fixedImage.nii")
