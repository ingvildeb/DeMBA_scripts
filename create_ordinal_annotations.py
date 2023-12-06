# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 02:11:14 2023

@author: ingvieb
"""
import nibabel as nib
from tqdm import tqdm
import numpy as np
import json

base_path = r"Z:/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/Volumes_for_elastix"
years = [2017, 2022]

for year in years:
    vol_path = rf"{base_path}/annotation_10_{year}_reoriented.nii.gz"
    vol = nib.load(vol_path)
    vol_data = vol.get_fdata()
    ids = np.unique(vol_data)
    ordinal_ids = np.arange(len(ids))
    id_map = {int(i):int(oid) for i,oid in zip(ids, ordinal_ids)}
    with open(rf"{base_path}/{year}_lookup.json", 'w') as out_json:
        json.dump(id_map, out_json)
    
    out_volume = np.zeros(vol_data.shape).astype(int)
    for i, oid in tqdm(id_map.items()):
        out_volume[vol_data == i] = int(oid)
    
    out_img = nib.Nifti1Image(out_volume, vol.affine, vol.header)
    out_img.set_data_dtype(np.uint32)
    out_filename = rf"{base_path}/ordinal_annotation_10_{year}_reoriented_int.nii"
    nib.save(out_img, out_filename)
        
