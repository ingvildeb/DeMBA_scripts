# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 02:11:14 2023

@author: ingvieb
"""
import nibabel as nib
from tqdm import tqdm
import numpy as np
import json

base_path = r"Z:\HBP_Atlasing\Developmental_atlases\DeMBA_Developmental mouse brain atlas\DeMBA-v1\01_working-environment\01_Data\Volumes_for_elastix\\"
years = [2017, 2022]

for year in years:
    vol_path = rf"{base_path}/annotation_10_{year}_reoriented.nii.gz"
    vol = nib.load(vol_path)
    vol_data = vol.get_fdata()
    ids = np.unique(vol_data)
    ordinal_ids = np.arange(len(ids))
    id_map = {i:oid for i,oid in zip(ids, ordinal_ids)}
    with open(f"{base_path}/{year}_lookup.json") as out_json:
        json.dump(id_map, out_json)
    
    out_volume = np.zeros(vol_data.shape)
    for i, oid in tqdm(id_map.values()):
        out_volume[vol_data == i] = oid
        
    out_img = nib.Nifti1Image(out_volume, vol_data.affine, vol_data.header)
    out_filename = rf"{base_path}/ordinal_annotation_10_{year}_reoriented.nii.gz"
    nib.save(out_img, out_filename)
        