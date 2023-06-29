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



def runTransform(fixedImage, movingImage, fixedPoints, movingPoints, movingSegmentation, resultTemplateName, resultSegmentationName):
    
    
    # elastix read fixed and moving images
    fixedImage = sitk.ReadImage(fixedImage)
    movingImage = sitk.ReadImage(movingImage)    
    
    ### DEFINE THE TRANSFORMATION
    
    # you can use the default parameter maps, e.g. for translation. however, if no default parameters are given, ElastixImageFilter will register our images with a 
    # translation -> affine -> b-spline multi-resolution approach by default.
    #parameterMap = sitk.GetDefaultParameterMap('translation')
    
    # AFFINE TRANSFORM PARAMETERS
    
    p_t = sitk.GetDefaultParameterMap('translation') 
    
    #p_t['Registration'] = ['MultiMetricMultiResolutionRegistration']
    p_t['Registration'] = ['MultiResolutionRegistration']
    
    # AFFINE TRANSFORM PARAMETERS
    
    p_a = sitk.GetDefaultParameterMap('affine')
    
    #ImageTypes
    p_a['FixedInternalImagePixelType'] = ['float']
    p_a['FixedImageDimension'] = ['3']
    p_a['MovingInternalImagePixelType'] = ['float']
    p_a['MovingImageDimension'] = ['3']
    
    
    #Components
    #p_a['Registration'] = ['MultiMetricMultiResolutionRegistration']
    p_a['Registration'] = ['MultiResolutionRegistration']
    
    p_a['FixedImagePyramid'] = ['FixedSmoothingImagePyramid']
    p_a['MovingImagePyramid'] = ['MovingSmoothingImagePyramid']
    p_a['Interpolator'] = ['BSplineInterpolator']
    p_a['Metric'] = ['AdvancedMattesMutualInformation']
    p_a['Optimizer'] = ['AdaptiveStochasticGradientDescent']
    p_a['ResampleInterpolator'] = ['FinalBSplineInterpolator']
    p_a['Resampler'] = ['DefaultResampler']
    p_a['Transform'] = ['AffineTransform']
    
    p_a['ErodeMask'] = ['false']
    
    p_a['NumberOfResolutions'] = ['4']
    
    p_a['HowToCombineTransforms'] = ['Compose']
    p_a['AutomaticTransformInitialization'] = ['true']
    p_a['AutomaticScalesEstimation'] = ['true']
    
    p_a['WriteTransformParametersEachIteration'] = ['false']
    
    p_a['MaximumNumberOfIterations'] = ['500']
    
    p_a['NumberOfHistogramBins'] = ['32']
    p_a['FixedLimitRangeRatio'] = ['0.0']
    p_a['MovingLimitRangeRatio'] = ['0.0']
    p_a['FixedKernelBSplineOrder'] = ['3']
    p_a['MovingKernelBSplineOrder'] = ['3']
    
    p_a['ImageSampler'] = ['RandomCoordinate']
    p_a['FixedImageBSplineInterpolationOrder'] = ['3']
    p_a['UseRandomSampleRegion'] = ['false']
    p_a['NumberOfSpatialSamples'] = ['4000']
    p_a['NewSamplesEveryIteration'] = ['true']
    p_a['CheckNumberOfSamples'] = ['true']
    p_a['MaximumNumberOfSamplingAttempts'] = ['10']
    p_a['BSplineInterpolationOrder'] = ['3']
    
    p_a['FinalBSplineInterpolationOrder'] = ['3']
    
    p_a['DefaultPixelValue'] = ['0']
    
    p_a['SP_A'] = ['20.0']
    
    
    # BSPLINE TRANSFORM PARAMETERS
    
    p_b = sitk.GetDefaultParameterMap('bspline') 
    
    
    #ImageTypes: 
    p_b['FixedInternalImagePixelType'] = ['float']
    p_b['FixedImageDimension'] = ['3']
    p_b['MovingInternalImagePixelType'] = ['float']
    p_b['MovingImageDimension'] = ['3']
    
    #Components: The following components should usually be left as they are. 
    
    p_b['Registration'] = ['MultiMetricMultiResolutionRegistration']
    p_b['Interpolator'] = ['BSplineInterpolator']
    p_b['ResampleInterpolator'] = ['FinalBSplineInterpolator']
    p_b['Resampler'] = ['DefaultResampler']
    
    
    # These may be changed to Fixed/MovingSmoothingImagePyramid. See the manual.
    
    p_b['FixedImagePyramid'] = ['FixedSmoothingImagePyramid']
    p_b['MovingImagePyramid'] = ['MovingSmoothingImagePyramid']
    
    
    # The following components are most important:
    # The optimizer AdaptiveStochasticGradientDescent (ASGD) works quite ok in general. 
    
    p_b['Optimizer'] = ['AdaptiveStochasticGradientDescent']
    
    # The Transform and Metric are important and need to be chosen careful for each application. See manual.
    p_b['Transform'] = ['BSplineTransform']
    p_b['Metric'] = ['AdvancedMattesMutualInformation',"CorrespondingPointsEuclideanDistanceMetric"]
    
    
    # If you do not use a mask, the option doesn't matter.
    p_b['ErodeMask'] = ['false']
    
    
    # The number of resolutions. 1 Is only enough if the expected deformations are small. 3 or 4 mostly works fine. For large images and large deformations, 5 or 6 may even be useful.
    
    p_b['NumberOfResolutions'] = ['3']
    
    
    # The control point spacing of the bspline transformation in the finest resolution level. Can be specified for each dimension differently. Unit: mm.
    # The lower this value, the more flexible the deformation. Low values may improve the accuracy, but may also cause unrealistic deformations. This is a very important setting!
    # We recommend tuning it for every specific application. It is difficult to come up with a good 'default' value.
    # Alternatively, the grid spacing can be specified in voxel units. To do that, uncomment the following line and comment/remove the FinalGridSpacingInPhysicalUnits definition.
    
    p_b['FinalGridSpacingInVoxels'] = ['50', '50', '50']
    
    # By default the grid spacing is halved after every resolution, such that the final grid spacing is obtained in the last resolution level. You can also specify your own schedule, if you uncomment the following line:
    p_b['GridSpacingSchedule'] = ['6','6','6','2.5','2.5','2.5','1','1','1']
    
    # Whether transforms are combined by composition or by addition. Generally, Compose is the best option in most cases. It does not influence the results very much.
    p_b['HowToCombineTransforms'] = ['Compose']
    
    
    # Maximum number of iterations in each resolution level. Maximum number of iterations in each resolution level: 200-2000 works usually fine for nonrigid registration. 
    # The more, the better, but the longer computation time. This is an important parameter!
    p_b['MaximumNumberOfIterations'] = ['5000']
    
    # Number of grey level bins in each resolution level, for the mutual information. 16 or 32 usually works fine. You could also employ a hierarchical strategy:(NumberOfHistogramBins 16 32 64)
    p_b['NumberOfHistogramBins'] = ['32']
    
    # # No documentation found:
    p_b['WriteTransformParametersEachIteration'] = ['false']
    
    p_b['FixedLimitRangeRatio'] = ['0.0']
    p_b['MovingLimitRangeRatio'] = ['0.0']
    p_b['FixedKernelBSplineOrder'] = ['3']
    p_b['MovingKernelBSplineOrder'] = ['3']
    
    p_b['FixedImageBSplineInterpolationOrder'] = ['1']
        
    #Set the NumberOfSpatialSamples to 3000. Don’t go lower than 2000.
    p_b['NumberOfSpatialSamples'] = ['10000']
    
    # Refresh these spatial samples in every iteration, and select them randomly. 
    p_b['ImageSampler'] = ['RandomCoordinate']
    p_b['NewSamplesEveryIteration'] = ['true']
    
    # An interesting option for the RandomCoordinate sampler is the UseRandomSampleRegion parameter, used in combination with the SampleRegionSize parameter. 
    # If UseRandomSampleRegion is set to "false" (the default), the sampler draws samples from the entire image domain
    
    # p_b['UseRandomSampleRegion'] = ['true']
    # p_b['SampleRegionSize'] = ['2.5', '2.5', '2.5']
    
    p_b['CheckNumberOfSamples'] = ['true']
    p_b['MaximumNumberOfSamplingAttempts'] = ['10']
    
    
    # Order of B-Spline interpolation used in each resolution level: 
    # It may improve accuracy if you set this to 3. Never use 0. An order of 1 gives linear interpolation. This is in most applications a good choice.
    p_b['BSplineInterpolationOrder'] = ['3']
    
    #Order of B-Spline interpolation used for applying the final deformation
    # 3 gives good accuracy; recommended in most cases. 0 gives worst accuracy, but is appropriate for binary images (masks, segmentations); equivalent to nearest neighbor interpolation.
    p_b['FinalBSplineInterpolationOrder'] = ['3']
    
    #Default pixel value for pixels that come from outside the picture
    p_b['DefaultPixelValue'] = ['0']
    
    
    p_b['UseRelativeWeights'] = ['true']
    p_b['Metric0Weight'] = ['5.0']
    
    
    ### APPLY TRANSFORMS
    
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.LogToFileOn()
    elastixImageFilter.SetFixedImage(fixedImage)
    elastixImageFilter.SetMovingImage(movingImage)    
    
    # leave out if no parameterMap is specified
    parameterMapVector = sitk.VectorOfParameterMap()
    parameterMapVector.append(p_t)
    parameterMapVector.append(p_a)
    parameterMapVector.append(p_b)
    elastixImageFilter.SetParameterMap(parameterMapVector)
    elastixImageFilter.RemoveParameter('FinalGridSpacingInPhysicalUnits')
    
    elastixImageFilter.SetFixedPointSetFileName(fixedPoints)
    elastixImageFilter.SetMovingPointSetFileName(movingPoints)
    #elastixImageFilter.AddParameter("Metric", "CorrespondingPointsEuclideanDistanceMetric")
    
    print("Executing elastix transformation...")
    # execute the transformation
    elastixImageFilter.Execute()
    
    print("Saving result image...")
    # save the resulting (transformed moving image) as a nii file
    resultImage = sitk.WriteImage(elastixImageFilter.GetResultImage(), resultTemplateName)
        
    
    ### TRANSFORM SEGMENTATION IMAGE IN SAME WAY
    
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
    
    
    
    transformixImageFilter.SetMovingImage(sitk.ReadImage(movingSegmentation))
    transformixImageFilter.Execute()
    outvolume = transformixImageFilter.GetResultImage()
    sitk.WriteImage(outvolume, resultSegmentationName)
    
    
fixedImage = r"D:\elastix_testing\P28_beta\function_test\P28_DeMBA_template.nii.gz"
movingImage = r"D:\elastix_testing\P28_beta\function_test\average_template_10_adjusted.nii.gz"
fixedPoints = r"D:\elastix_testing\P28_beta\function_test\P28_points.pts"
movingPoints = r"D:\elastix_testing\P28_beta\function_test\adult_points.pts"
movingSegmentation = r"D:\elastix_testing\P28_beta\function_test\annotation_10_adjusted.nii.gz"
resultTemplateName = r"D:\elastix_testing\P28_beta\function_test\resultTemplate"
resultSegmentationName = r"D:\elastix_testing\P28_beta\function_test\resultSegmentation"