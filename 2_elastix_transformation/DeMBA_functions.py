# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 14:50:20 2023

@author: ingvieb
"""

import SimpleITK as sitk
import numpy as np
import nibabel as nib
import json
import os 
from tkinter import *  


def LMRtoElastixPoints(filepath, fixedAge, movingAge):
    
    with open(filepath) as file:
        openFile = json.load(file)
    try:
        xyz_list = [(i["px"], i["py"], i["pz"]) for i in openFile]
    except KeyError:
        raise Exception("you didnt set all the target points in LMR dummy")
        
    output_file_dir = os.path.dirname(filepath)
        
    fixedPointsPath = output_file_dir + "//" + fixedAge + '_points.pts'
    movingPointsPath = output_file_dir + "//" + movingAge + '_points.pts'
    
    with open(fixedPointsPath, 'w') as f:
        f.write("index")
        f.write('\n')    
        f.write(str(len(xyz_list)))
        f.write('\n')
        
        for point in xyz_list:
            
            f.write(f"{round(point[0])} {round(point[1])} {round(point[2])}\n")
            
        
    xyz_list = [(i["x"], i["y"], i["z"]) for i in openFile]

    
    with open(movingPointsPath, 'w') as f:
        f.write("index")
        f.write('\n')    
        f.write(str(len(xyz_list)))
        f.write('\n')
        
        for point in xyz_list:
            
            f.write(f"{round(point[0])} {round(point[1])} {round(point[2])}\n")
            
    return fixedPointsPath, movingPointsPath



def createParameterMap(file, regType):
    
    with open(file, 'r') as f:
        param_dict = json.load(f)
    
    pMap = sitk.GetDefaultParameterMap(regType) 
        
    for key, value in param_dict.items():
        pMap[key] = value
    
    return pMap


def runTransform(fixedAge, fixedImage, movingImage, fixedPoints, movingPoints, movingSegmentation, resultTemplateName, resultSegmentationName, deformationName):
    
    # elastix read fixed and moving images
    fixedImage = sitk.ReadImage(fixedImage)
    movingImage = sitk.ReadImage(movingImage)   
       
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.LogToFileOn()
    elastixImageFilter.SetFixedImage(fixedImage)
    elastixImageFilter.SetMovingImage(movingImage)    
    
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
    
    elastixImageFilter.SetFixedPointSetFileName(fixedPoints)
    elastixImageFilter.SetMovingPointSetFileName(movingPoints)
    
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
    
    for mSeg, rSegName in zip(movingSegmentation, resultSegmentationName):
        transformixImageFilter.SetMovingImage(sitk.ReadImage(mSeg))
        transformixImageFilter.Execute()
        sitk.WriteImage(transformixImageFilter.GetResultImage(), rSegName)
        print(f"Finished processing {mSeg}")
    
    # save the deformation field
    deformationField = transformixImageFilter.GetDeformationField()
    sitk.WriteImage(deformationField, deformationName) 
    
    
    print("Finished all processing")

    
    