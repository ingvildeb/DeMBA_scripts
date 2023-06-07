# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 20:00:08 2023

@author: ingvieb
"""

import nibabel as nib
import numpy as np
volPath = r'C:\Users\ingvieb\Elastix_testing\P07_second\P07_brain_resample_reoriented.nii'
outputFilename = r'C:\Users\ingvieb\Elastix_testing\P07_third\P07_brain_resample_reoriented_microns.nii'

volPath = r'C:\Users\ingvieb\Elastix_testing\P07_second\2023-04-04_LMR-registration_P07_avg_nl.nii'
outputFilename = r'C:\Users\ingvieb\Elastix_testing\P07_third\2023-04-04_LMR-registration_P07_avg_nl.nii_microns.nii'

volPath = r'C:\Users\ingvieb\Elastix_testing\P07_second\2023-04-04_LMR-registration_P07_seg_nl.nii'
outputFilename = r'C:\Users\ingvieb\Elastix_testing\P07_third\2023-04-04_LMR-registration_P07_seg_nl.nii_microns.nii'

nibfile = nib.load(volPath)
header = nibfile.header
header.set_xyzt_units(2)

#pixdim = nibfile.header.get('pixdim')
affineTransform = np.array([[1000.,  1.,  1.,  1.],
                            [ 1., 1000.,  1.,  1.],
                            [ 1.,  1., 1000.,  0.],
                            [ 1.,  1.,  1.,  1.]])


header["pixdim"][1:4] = header["pixdim"][1:4] * 1000

#new niftiimage
outputVol = nib.Nifti1Image(nibfile.get_fdata(), nibfile.affine * affineTransform, header)
print('new pixdim', outputVol.header["pixdim"])





nib.save(outputVol ,outputFilename)


secondNibFile = nib.load(outputFilename)

secondNibFile.header.get('pixdim')
