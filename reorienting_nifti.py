# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 17:14:24 2023

@author: ingvieb
"""


import nibabel as nib
import numpy as np


## transform CCF
volume_og_CCF = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\annotation_10.nii.gz')
data = volume_og_CCF.get_fdata()
# change the order of the axes
data = np.transpose(data, (2,0,1))




# flip two of the axes
data = data[:, ::-1, ::-1]
# write the new volume

reoriented_data_CCF = nib.Nifti1Image(data, volume_og_CCF.affine, volume_og_CCF.header)

nib.save(reoriented_data_CCF, r'C:\Users\ingvieb\Elastix_testing\re-orienting\annotation_10_reoriented.nii.gz')


## TRANSFORM P28
volume_og_P28 = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\P28_brain_resampled_reoriented.nii')
data = volume_og_P28.get_fdata()
# change the order of the axes
data = np.transpose(data, (2,0,1))
# flip two of the axes
data = data[:, ::-1, ::-1]
# write the new volume

reoriented_data_P28 = nib.Nifti1Image(data, volume_og_P28.affine, volume_og_P28.header)

reoriented_data_P28 = reoriented_data_P28.get_fdata()

import matplotlib.pyplot as plt
newslice = reoriented_data_P28[378,:,:]
plt.imshow(newslice, cmap='magma', vmin=0, vmax=1500)
plt.show()

#nib.save(reoriented_data_CCF, r'C:\Users\ingvieb\Elastix_testing\re-orienting\annotation_10_reoriented.nii.gz')



target_vol = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\2023-04-04_LMR-registration_P28_avg_nl.nii').get_fdata()
targetslice = target_vol[209,:,:]
plt.imshow(targetslice, cmap='magma', vmin=0, vmax=1500)
plt.show()



CCFvol_nib = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\average_template_10.nii.gz')
CCFvol = CCFvol_nib.get_fdata()
CCFvol = np.transpose(CCFvol, (2,1,0))

header = CCFvol_nib.header
header.set_xyzt_units(2)
CCFvol_reoriented = nib.Nifti1Image(CCFvol, np.eye(4), header)

CCFvol_reoriented = nib.Nifti1Image(CCFvol, np.eye(4), CCFvol_nib.header)
nib.save(CCFvol_reoriented, r'C:\Users\ingvieb\Elastix_testing\re-orienting\average_template_10_reoriented_FINAL_eye_xyzt.nii.gz')

CCFslice = CCFvol[:,:,378]
plt.imshow(CCFslice, cmap='magma', vmin=0, vmax=2500)
plt.show()



CCFvol_nib = nib.load(r'C:\Users\ingvieb\Elastix_testing\re-orienting\annotation_10.nii.gz')
CCFvol = CCFvol_nib.get_fdata()
CCFvol = np.transpose(CCFvol, (2,1,0))
header = CCFvol_nib.header
header.set_xyzt_units(2)
CCFvol_reoriented = nib.Nifti1Image(CCFvol, np.eye(4), header)
nib.save(CCFvol_reoriented, r'C:\Users\ingvieb\Elastix_testing\re-orienting\annotation_10_reoriented_FINAL_eye_header_set_xyzt.nii.gz')

CCFslice = CCFvol[:,:,378]
plt.imshow(CCFslice, cmap='magma', vmin=0, vmax=2500)
plt.show()




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
nib.save(P28vol_reoriented, r'C:\Users\ingvieb\Elastix_testing\re-orienting\P28_reoriented_FINAL_eye_header_set_xyzt_multiplied_pixdim_double_scale_affine.nii.gz')


P28slice = P28vol[:,:,209]
plt.imshow(P28slice, cmap='magma', vmin=0, vmax=2500)
plt.show()



vol1 = nib.load(r'C:\Users\ingvieb\Elastix_testing\P28\P28_reoriented_FINAL.nii.gz').get_fdata()

resultslice = vol1[:,:,209]
plt.imshow(resultslice, cmap='magma', vmin=0, vmax=2500)
plt.show()


vol2 = nib.load(r'C:\Users\ingvieb\Elastix_testing\P28\average_template_10_reoriented_FINAL.nii.gz').get_fdata()

resultslice = vol2[:,:,378]
plt.imshow(resultslice, cmap='magma', vmin=0, vmax=2500)
plt.show()



vol3 = nib.load(r'C:\Users\ingvieb\Elastix_testing\P28\annotation_10_reoriented_FINAL.nii.gz').get_fdata()

resultslice = vol3[:,:,378]
plt.imshow(resultslice, cmap='magma', vmin=0, vmax=2500)
plt.show()



gergely_allen = r"C:\Users\ingvieb\Elastix_testing\archive\P28_second//2023-04-04_LMR-registration_P28_avg_nl.nii"
gergely_allen = nib.load(gergely_allen)