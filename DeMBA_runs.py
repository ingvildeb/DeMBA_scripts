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

path = r"C:\Users\ingvieb\elastix_testing\reoriented_data//"
fixedAge = "P7"
# give the paths of the volumes to be used as fixedImage and movingImage. in this case, the CCFvolume will be the moving and the DeMBA volume will be the fixed.

movingImage = f"{path}/{fixedAge}/DeMBA_P14_brain.nii"
movingSegmentation = [f"{path}/{fixedAge}/P14_resultSegmentation_2017.nii", f"{path}/{fixedAge}/P14_resultSegmentation_2022.nii"]
fixedImage = f"{path}/{fixedAge}/DeMBA_{fixedAge}_brain.nii"
fixedPoints = f"{path}/{fixedAge}/fixed.pts"
movingPoints = f"{path}/{fixedAge}/moving.pts"


runsdir = fr"{path}/{fixedAge}/runs/"
numberofruns = len(glob(fr"{runsdir}/*"))
fullrunsdir = fr"{runsdir}run{numberofruns}/"
os.mkdir(fullrunsdir)

resultTemplateName = f"{fullrunsdir}/resultTemplate.nii"
resultSegmentationName = [f"{fullrunsdir}/{fixedAge}_resultSegmentation_2017.nii", f"{fullrunsdir}/{fixedAge}_resultSegmentation_2022.nii"]
deformationName = f"{fullrunsdir}/deformationField.nii"

# add th4 time stamp 
time = datetime.datetime.now()
# format time stamp
time = time.strftime("%d-%m-%Y %H:%M:%S")

# format
message = f"""
{time} \n
Running P14 - P7 with the volumes that have correct IDs.

"""
# write to file
with open(f"{fullrunsdir}notes.txt", "w") as f:
    f.write(message)
    


dfs.runTransform(fixedAge, fixedImage, movingImage, fixedPoints, movingPoints, movingSegmentation, resultTemplateName, resultSegmentationName, deformationName)

    
shutil.copy(fixedPoints, f"{fullrunsdir}fixed.pts")
shutil.copy(movingPoints, f"{fullrunsdir}moving.pts")
shutil.copy("elastix.log", f"{fullrunsdir}elastix.log")
shutil.copy("TransformParameters.0.txt", f"{fullrunsdir}TransformParameters.0.txt")
shutil.copy("TransformParameters.1.txt", f"{fullrunsdir}TransformParameters.1.txt")
shutil.copy("TransformParameters.2.txt", f"{fullrunsdir}TransformParameters.2.txt")
shutil.copy(f"{fixedAge}_parameter_jsons/param_dict_t.json", f"{fullrunsdir}param_dict_t.json")
shutil.copy(f"{fixedAge}_parameter_jsons/param_dict_a.json", f"{fullrunsdir}param_dict_a.json")
shutil.copy(f"{fixedAge}_parameter_jsons/param_dict_b.json", f"{fullrunsdir}param_dict_b.json")
shutil.copy("DeMBA_runs.py", f"{fullrunsdir}script.py")
shutil.copy(movingImage, f"{fullrunsdir}movingImage.nii")
shutil.copy(fixedImage, f"{fullrunsdir}fixedImage.nii")
