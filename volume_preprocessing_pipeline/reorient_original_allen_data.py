import nrrd
import nibabel as nib
import numpy as np
from glob import glob 
import matplotlib.pyplot as plt
header = {
    "xyzt_units": "microns",
    "spacings": np.array([0.01, 0.01, 0.01]),

}
base_path = r"Y:\harry_temp\demba\original_data\\"
save_path = r"Y:\harry_temp\demba\reoriented_data\\"
#caudoputamin should be 672
path = rf"{base_path}\average_template_10.nrrd"
img, header = nrrd.read(path)
img = img.transpose(2,1,0)
#convert to nii
img = nib.Nifti1Image(img, np.eye(4))
#include header
header = img.header 
header.set_xyzt_units(xyz=2, t=0)
header['pixdim'][1:4] = np.array([0.01, 0.01, 0.01])
nib.save(img, rf"{save_path}\average_template_10_reoriented.nii.gz")

path = rf"{base_path}\annotation_10_2017.nrrd"
img, header = nrrd.read(path)
img = img.transpose(2,1,0)
img = nib.Nifti1Image(img, np.eye(4))
header = img.header
header.set_xyzt_units(xyz=2, t=0)   
header['pixdim'][1:4] = np.array([0.01, 0.01, 0.01])
nib.save(img, rf"{save_path}\annotation_10_2017_reoriented.nii.gz")

path = rf"{base_path}\annotation_10_2022.nrrd"
img, header = nrrd.read(path)
img = img.transpose(2,1,0)
img = nib.Nifti1Image(img, np.eye(4))
header = img.header
header.set_xyzt_units(xyz=2, t=0)
header['pixdim'][1:4] = np.array([0.01, 0.01, 0.01])
nib.save(img, rf"{save_path}\annotation_10_2022_reoriented.nii.gz")
