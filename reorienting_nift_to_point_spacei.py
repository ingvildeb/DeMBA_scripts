# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 17:14:24 2023

@author: ingvieb
"""


import nibabel as nib
import numpy as np


path = r'C:\Users\ingvieb\Elastix_testing\re-orienting\reorient_to_points/'


## transform CCF
volume_og_CCF = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\annotation_10.nii.gz')
data = volume_og_CCF.get_fdata()
# change the order of the axes
data = np.transpose(data, (2,1,0))
reoriented_data_CCF = nib.Nifti1Image(data, volume_og_CCF.affine, volume_og_CCF.header)
nib.save(reoriented_data_CCF, rf'{path}/annotation_10_reoriented.nii.gz')




CCFvol_nib = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\average_template_10.nii.gz')
CCFvol = CCFvol_nib.get_fdata()
CCFvol = np.transpose(CCFvol, (2,1,0))

header = CCFvol_nib.header
header.set_xyzt_units(2)

CCFvol_reoriented = nib.Nifti1Image(CCFvol, np.eye(4), CCFvol_nib.header)
nib.save(CCFvol_reoriented, rf'{path}/average_template_10_reoriented_FINAL_eye_xyzt.nii.gz')




CCFvol_nib = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\annotation_10.nii.gz')
CCFvol = CCFvol_nib.get_fdata()
CCFvol = np.transpose(CCFvol, (2,1,0))
header = CCFvol_nib.header
header.set_xyzt_units(2)
CCFvol_reoriented = nib.Nifti1Image(CCFvol, np.eye(4), header)
nib.save(CCFvol_reoriented, rf'{path}/annotation_10_reoriented_FINAL_eye_header_set_xyzt.nii.gz')





P28vol_nib = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\P28_brain_resampled_reoriented.nii')
P28vol = P28vol_nib.get_fdata()
P28vol = np.transpose(P28vol, (0,2,1))
P28vol = P28vol[:, ::-1, ::-1]

double_scale_affine = np.array([
       [2., 0., 0., 0.],
       [0., 2., 0., 0.],
       [0., 0., 2., 0.],
       [0., 0., 0., 1.]])

header = P28vol_nib.header
header.set_xyzt_units(2)
#i dont think changing pixdims affects the actual header but yolo
header["pixdim"][1:4] = header["pixdim"][1:4] * 1000


P28vol_reoriented = nib.Nifti1Image(P28vol, double_scale_affine, header)
nib.save(P28vol_reoriented,rf'{path}/P28_reoriented_FINAL_eye_header_set_xyzt_multiplied_pixdim_double_scale_affine.nii.gz')





