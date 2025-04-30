"""
For visualisation purposes it was necessary to set the area outside the brain negative
"""
import nibabel as nib
from tqdm import tqdm

root = "/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/"

for age in tqdm([4, 6, 9, 20, 28, 56]):
    paths = [
            f"{root}/interpolated_volumes/calb1_gene_expression_volumes/DeMBA_P{age}_calb1.nii.gz"]
    # if age == 4:
    #     paths.append(f"{root}/interpolated_volumes/adult_calbindin_warped_down_20um/adult_calb1_to_p{age}.nii.gz",)
    atlas_path = f"{root}/interpolated_segmentations/AllenCCFv3_segmentations/20um/2017/DeMBA_P{age}_segmentation_2017_20um.nii.gz"
    atlas_img = nib.load(atlas_path)
    atlas_arr = atlas_img.get_fdata()
    atlas_mask = atlas_arr == 0
    for path in paths:
        img = nib.load(path)
        arr = img.get_fdata()
        arr[atlas_mask] = -1
        out_img = nib.Nifti1Image(arr, header = img.header, affine= img.affine)
        out_path = path.replace(f"{root}/interpolated_volumes/calb1_gene_expression_volumes/", 
                                f"{root}/additional_not_for_dataset/negative_background_for_figure/")
        nib.save(out_img, out_path)
    out_img = nib.Nifti1Image(atlas_mask, header = atlas_img.header, affine= atlas_img.affine)
    out_path = f"{root}/additional_not_for_dataset/glass_brain/allen_p{age}_mask.nii.gz"
    nib.save(out_img, out_path)