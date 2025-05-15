import nrrd
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
age = 17
atlas_path = rf"/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/interpolated_segmentations/AllenCCFv3_segmentations/20um/2017/DeMBA_P{age}_segmentation_2017_20um.nii.gz"
atlas_img = nib.load(atlas_path)
atlas_arr = np.asanyarray(atlas_img.dataobj)
midpoint = np.array(atlas_arr.shape) // 2
atlas_arr[:midpoint[0],:midpoint[1],:midpoint[2]] = 0
out_img = nib.Nifti1Image(atlas_arr, header = atlas_img.header, affine= atlas_img.affine)
out_path = f"../data_files/allen_p{age}_cutout.nii.gz"
nib.save(out_img, out_path)