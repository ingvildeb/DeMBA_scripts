"""
For visualisation purposes it was necessary to set the area outside the brain negative
"""
import nibabel as nib
paths = ["/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/interpolated_volumes/adult_calbindin_warped_down_20um/adult_calb1_to_p4.nii.gz",
         "/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/interpolated_volumes/calbindin_gene_expression_20um/calb1_gene_volume_P4_20micron.nii.gz"]
atlas_path = r"/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/interpolated_segmentations/AllenCCFv3_segmentations/20um/2017/DeMBA_P4_segmentation_2017_20um.nii.gz"
atlas_img = nib.load(atlas_path)
atlas_arr = atlas_img.get_fdata()
atlas_mask = atlas_arr == 0
for path in paths:
    img = nib.load(path)
    arr = img.get_fdata()
    arr[atlas_mask] = -1
    out_img = nib.Nifti1Image(arr, header = img.header, affine= img.affine)
    out_path = path.replace("/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/interpolated_volumes/", 
                            "/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/negative_background_for_figure/")
    nib.save(out_img, out_path)

import nrrd

atlas_path = r"../data_files/annotation_25.nrrd"
atlas_arr, header = nrrd.read(atlas_path)
atlas_mask = atlas_arr == 0

out_img = nib.Nifti1Image(atlas_mask, header = atlas_img.header, affine= atlas_img.affine)
out_path = "../data_files/allen_p56_mask.nii.gz"
nib.save(out_img, out_path)