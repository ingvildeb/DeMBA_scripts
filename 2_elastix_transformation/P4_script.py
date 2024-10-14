# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:27:23 2023

@author: ingvieb
"""


from glob import glob
import shutil
import datetime
import SimpleITK as sitk
import numpy as np
import nibabel as nib
import json
import os 


def createParameterMap(file, regType):
    
    with open(file, 'r') as f:
        param_dict = json.load(f)
    
    pMap = sitk.GetDefaultParameterMap(regType) 
        
    for key, value in param_dict.items():
        pMap[key] = value
    
    return pMap



path = r"C:\Users\ingvieb\elastix//"
fixedAge = "P4"
movingAge = "P7"
# give the paths of the volumes to be used as fixedImage and movingImage. in this case, the CCFvolume will be the moving and the DeMBA volume will be the fixed.
movingImagePath = f"{path}/{fixedAge}/DeMBA_{movingAge}_result_brain.nii.gz"

movingSegmentation = [f"{path}/{fixedAge}/{movingAge}_resultSegmentation_2017.nii.gz", 
                      f"{path}/{fixedAge}/{movingAge}_resultSegmentation_2022.nii.gz",
                      ]

fixedImagePath = f"{path}/{fixedAge}/DeMBA_{fixedAge}_brain.nii.gz"
fixedPointsPath = f"{path}/{fixedAge}/fixed.pts"
movingPointsPath = f"{path}/{fixedAge}/moving.pts"


runsdir = fr"{path}/{fixedAge}/runs/"
numberofruns = len(glob(fr"{runsdir}/*"))
fullrunsdir = fr"{runsdir}run{numberofruns}/"
os.makedirs(fullrunsdir, exist_ok=True)

resultTemplateName = f"{fullrunsdir}/resultTemplate.nii.gz"
resultSegmentationName = [f"{fullrunsdir}/{fixedAge}_resultSegmentation_2017.nii.gz", 
                          f"{fullrunsdir}/{fixedAge}_resultSegmentation_2022.nii.gz",]


deformationName = f"{fullrunsdir}/deformationField.nii.gz"



# add th4 time stamp 
time = datetime.datetime.now()
# format time stamp
time = time.strftime("%d-%m-%Y %H:%M:%S")

# format
message = f"""
{time} \n
Running transformation of {movingAge} to {fixedAge}.

"""
# write to file
with open(f"{fullrunsdir}notes.txt", "w") as f:
    f.write(message)
    




# elastix read fixed and moving images
fixedImage = sitk.ReadImage(fixedImagePath)
movingImage = sitk.ReadImage(movingImagePath)   

fixedImages = [fixedImage]
movingImages = [movingImage]



elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.LogToFileOn()
elastixImageFilter.SetFixedImage(fixedImages)
elastixImageFilter.SetMovingImage(movingImages)    



# define the transformation maps

p_t = createParameterMap(fr"{fixedAge}_parameter_jsons/param_dict_t.json", "translation")
p_a = createParameterMap(fr"{fixedAge}_parameter_jsons/param_dict_a.json", "affine")
p_b = createParameterMap(fr"{fixedAge}_parameter_jsons/param_dict_b.json", "bspline")

parameterMapVector = sitk.VectorOfParameterMap()
parameterMapVector.append(p_t)
parameterMapVector.append(p_a)
parameterMapVector.append(p_b)

elastixImageFilter.SetParameterMap(parameterMapVector)
elastixImageFilter.RemoveParameter('FinalGridSpacingInPhysicalUnits')

# add points to the registration

elastixImageFilter.SetFixedPointSetFileName(fixedPointsPath)
elastixImageFilter.SetMovingPointSetFileName(movingPointsPath)
elastixImageFilter.SetOutputDirectory(fullrunsdir)
print("Executing elastix transformation...")
# execute the transformation
elastixImageFilter.Execute()

print("Saving result image...")
# save the resulting (transformed moving image) as a nii file
sitk.WriteImage(elastixImageFilter.GetResultImage(), resultTemplateName)
    
# transform segmentation image in the same way

print("Preparing transform parameters...")

transformParameterMap = elastixImageFilter.GetTransformParameterMap()

# this command ensures that there is no interpolation between labels, important because otherwise it will create average ids for the voxels at borders of two regions.
# include one of these lines for each parameter map.
transformParameterMap[0]['FinalBSplineInterpolationOrder'] = ['0']
transformParameterMap[1]['FinalBSplineInterpolationOrder'] = ['0']
transformParameterMap[2]['FinalBSplineInterpolationOrder'] = ['0']


print("Applying transform to segmentation...")
transformixImageFilter = sitk.TransformixImageFilter()
transformixImageFilter.ComputeDeformationFieldOn()
transformixImageFilter.SetTransformParameterMap(transformParameterMap)

from skimage import feature
from tqdm import tqdm



def create_outline(path, save_path):
    img = nib.load(path)
    # Get the data from the image
    data = img.get_fdata()
    # Assuming 'data' is your 3D numpy array
    edges = np.empty_like(data)
    pbar = tqdm(total=data.shape[0] + data.shape[1] + data.shape[2])
    for i in range(data.shape[0]):
        edges[i] = feature.canny(data[i])
        pbar.update(1)

    for i in range(data.shape[1]):
        edges[:, i] += feature.canny(data[:, i])
        pbar.update(1)

    for i in range(data.shape[2]):
        edges[:, :, i] += feature.canny(data[:, :, i])
        pbar.update(1)
    edges[edges > 0] = 1
    pbar.close()
    nib.save(nib.Nifti1Image(edges, img.affine, img.header), save_path)

for mSeg, rSegName in zip(movingSegmentation, resultSegmentationName):
    transformixImageFilter.SetMovingImage(sitk.ReadImage(mSeg))
    transformixImageFilter.Execute()
    sitk.WriteImage(transformixImageFilter.GetResultImage(), rSegName)
    create_outline(rSegName, rSegName.replace(".nii.gz", "_outline.nii.gz"))
    print(f"Finished processing {mSeg}")

# save the deformation field
deformationField = transformixImageFilter.GetDeformationField()
sitk.WriteImage(deformationField, deformationName) 


print("Finished all processing")

    
shutil.copy(fixedPointsPath, f"{fullrunsdir}fixed.pts")
shutil.copy(movingPointsPath, f"{fullrunsdir}moving.pts")
shutil.copy("elastix.log", f"{fullrunsdir}elastix.log")
shutil.copy("TransformParameters.0.txt", f"{fullrunsdir}TransformParameters.0.txt")
shutil.copy("TransformParameters.1.txt", f"{fullrunsdir}TransformParameters.1.txt")
shutil.copy("TransformParameters.2.txt", f"{fullrunsdir}TransformParameters.2.txt")
shutil.copy(f"{fixedAge}_parameter_jsons/param_dict_t.json", f"{fullrunsdir}param_dict_t.json")
shutil.copy(f"{fixedAge}_parameter_jsons/param_dict_a.json", f"{fullrunsdir}param_dict_a.json")
shutil.copy(f"{fixedAge}_parameter_jsons/param_dict_b.json", f"{fullrunsdir}param_dict_b.json")
shutil.copy("P4_script.py", f"{fullrunsdir}script.py")
shutil.copy(movingImagePath, f"{fullrunsdir}movingImage.nii.gz")
shutil.copy(fixedImagePath, f"{fullrunsdir}fixedImage.nii.gz")
#shutil.copy(fixedManualSegName, f"{fullrunsdir}fixedManualSeg.nii.gz")
#shutil.copy(movingManualSegName, f"{fullrunsdir}movingManualSeg.nii.gz")
