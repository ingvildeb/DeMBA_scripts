# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 02:11:14 2023

@author: ingvieb
"""
import nibabel as nib
from tqdm import tqdm
import numpy as np
import json

base_path = r"Z:/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/Volumes_for_elastix/"
base_vol_path = r"Z:/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/Volumes_warped/"

years = [2017, 2022]

for year in years[1:]:
    vol_path = rf"{base_vol_path}/annotation_10_{year}_reoriented_warp_ordinal.nii.gz"
    vol = nib.load(vol_path)
    vol_data = vol.get_fdata()

    with open(rf"{base_path}/{year}_lookup.json", 'r') as in_json:
        id_map = json.load(in_json)
    
    out_volume = np.zeros(vol_data.shape)
    for i, oid in tqdm(id_map.items()):
        out_volume[vol_data == oid] = i
        
    out_img = nib.Nifti1Image(out_volume, vol.affine, vol.header)
    out_filename = rf"{base_vol_path}/annotation_10_{year}_reoriented_warp_original_id.nii.gz"
    nib.save(out_img, out_filename)
        


