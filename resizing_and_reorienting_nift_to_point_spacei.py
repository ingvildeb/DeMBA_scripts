# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 17:14:24 2023

@author: ingvieb
"""


import nibabel as nib
import numpy as np


path = r'C:\Users\ingvieb\Elastix_testing\re-orienting\ingvild_test/'

from scipy.ndimage import zoom




P28vol_nib = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\P28_brain_resampled_reoriented.nii')
P28vol = P28vol_nib.get_fdata()
P28vol = np.transpose(P28vol, (0,2,1))
P28vol = P28vol[:, ::-1, ::-1]

double_scale_affine = np.array([
       [2., 0., 0., 0.],
       [0., 2., 0., 0.],
       [0., 0., 2., 0.],
       [0., 0., 0., 2.]])

header = P28vol_nib.header
header.set_xyzt_units(2)
#i dont think changing pixdims affects the actual header but yolo
header["pixdim"][1:4] = header["pixdim"][1:4] * 1000


P28vol_reoriented = nib.Nifti1Image(P28vol, double_scale_affine, header)
nib.save(P28vol_reoriented,rf'{path}/P28_reoriented_FINAL_eye_header_set_xyzt_multiplied_pixdim_double_scale_affine.nii.gz')

target_shape = np.array(P28vol.shape)

## transform CCF template volume

CCFvol_nib = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\average_template_10.nii.gz')
CCFvol = CCFvol_nib.get_fdata()
CCFvol = np.transpose(CCFvol, (2,1,0))

header = CCFvol_nib.header
header.set_xyzt_units(2)
scale_ratio = target_shape/np.array(CCFvol.shape)
CCFvol = zoom(CCFvol, scale_ratio)
CCFvol_reoriented = nib.Nifti1Image(CCFvol, np.eye(4) * 2, CCFvol_nib.header)
nib.save(CCFvol_reoriented, rf'{path}/average_template_10_reoriented_FINAL_eye_xyzt.nii.gz')



## transform CCF segmentation volume

CCFvol_nib = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\annotation_10.nii.gz')
CCFvol = CCFvol_nib.get_fdata()
CCFvol = np.transpose(CCFvol, (2,1,0))

scale_ratio = target_shape/np.array(CCFvol.shape)
CCFvol = zoom(CCFvol, scale_ratio, order=0)

header = CCFvol_nib.header
header.set_xyzt_units(2)
CCFvol_reoriented = nib.Nifti1Image(CCFvol, np.eye(4) * 2, header)
nib.save(CCFvol_reoriented, rf'{path}/annotation_10_reoriented_FINAL_eye_header_set_xyzt.nii.gz')







