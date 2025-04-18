import nibabel as nib
import numpy as np
ages = [4, 9, 14, 28, 56]

data_path = r"/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/interpolated_segmentations/AllenCCFv3_segmentations/20um/2017/"
template_string = r"DeMBA_P{}_segmentation_2017_20um.nii.gz"
out_path = r"/mnt/z//HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/02_Figures/Figure4/"
for age in ages:
    img = nib.load(f"{data_path}/{template_string.format(age)}")
    arr = np.asanyarray(img.dataobj)
    glass = arr!=0
    out_img = nib.Nifti1Image(glass, img.affine, img.header)
    nib.save(
        out_img, 
        f"{out_path}/brain_label_{template_string.format(age)}"
    )
