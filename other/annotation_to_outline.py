import nibabel as nib
from glob import glob
import numpy as np
from scipy.ndimage import binary_erosion
from tqdm import tqdm

anno_path = r"/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/interpolated_segmentations/AllenCCFv3_segmentations/20um/"
files = glob(f"{anno_path}/2022/*")


for file in files:
    age = file.split("/")[-1].split("_")[1]
    print(f"age: {age}")
    img = nib.load(file)
    arr = img.get_fdata()
    # Create an empty array to store edges
    edges = np.zeros_like(arr)
    # Detect edges by comparing the original array with its eroded version
    for label in tqdm(np.unique(arr)):
        if label == 0:
            continue  # Skip background
        region = arr == label
        eroded_region = binary_erosion(region)
        edges += region & ~eroded_region
    # Save the edges volume as a new NIfTI image
    edges_img = nib.Nifti1Image(edges.astype(np.uint8), img.affine)
    nib.save(edges_img, f"{age}_edges_volume.nii")
