import CCF_translator
import nibabel as nib
from tqdm import tqdm

gubra_path = r"/home/harryc/github/gubra/Multimodal_mouse_brain_atlas_files"
start = 12 # 4




mri_img = nib.load(rf"{gubra_path}/MRI_space_oriented/mri_temp.nii.gz")
mri_arr = mri_img.get_fdata()

for age in tqdm(range(start, 57)):
    mri_ccf = CCF_translator.Volume(
        values = mri_arr.copy(), 
        space="perens_mri_mouse",
        age_PND=56,
            voxel_size_micron=25
        )
    mri_ccf.transform(
            target_age=age,
            target_space="demba_dev_mouse"
        )
    mri_ccf.save(
            f"../data_files/mri_p{age}.nii.gz"
        )
    
lsfm_img = nib.load(rf"{gubra_path}/LSFM_space_oriented/lsfm_temp.nii.gz")
lsfm_arr = lsfm_img.get_fdata()


for age in tqdm(range(start, 57)):
    lsfm_ccf = CCF_translator.Volume(
        values = lsfm_arr.copy(), 
        space="perens_lsfm_mouse",
        age_PND=56,
            voxel_size_micron=25
        )
    lsfm_ccf.transform(
            target_age=age,
            target_space="demba_dev_mouse"
        )
    lsfm_ccf.save(
            f"../data_files/lsfm_p{age}.nii.gz"
        )
    


gene_img = nib.load(rf"../data_files/calb1_gene_volume_P56_20micron.nii.gz")
gene_arr = gene_img.get_fdata()


for age in tqdm(range(start, 57)):
    gene_ccf = CCF_translator.Volume(
        values = gene_arr.copy(), 
        space="demba_dev_mouse",
        age_PND=56,
            voxel_size_micron=20
        )
    gene_ccf.transform(
            target_age=age,
            target_space="demba_dev_mouse"
        )
    gene_ccf.save(
            f"../data_files/adult_calb1_to_p{age}.nii.gz"
        )