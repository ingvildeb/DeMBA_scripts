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
ages = ["P7", "P14", "P21", "P28"]

for age in ages:
    for year in years:
        vol_path = rf"Z:\HBP_Atlasing\Developmental_atlases\DeMBA_Developmental mouse brain atlas\DeMBA-v1\01_working-environment\01_Data\DeMBA_v2\{age}\script_with_metadata\{age}_resultSegmentation_{year}.nii.gz"
        vol = nib.load(vol_path)
        vol_data = vol.get_fdata()
        vol_data = vol_data.astype(int)

        with open(rf"{base_path}/{year}_lookup.json", "r") as in_json:
            id_map = json.load(in_json)

        out_volume = np.zeros(vol_data.shape).astype(int)
        for i, oid in tqdm(id_map.items()):
            out_volume[vol_data == oid] = int(i)

        out_img = nib.Nifti1Image(out_volume, vol.affine, vol.header)
        out_img.set_data_dtype(np.uint32)
        out_filename = rf"Z:\HBP_Atlasing\Developmental_atlases\DeMBA_Developmental mouse brain atlas\DeMBA-v1\01_working-environment\01_Data\DeMBA_v2\{age}\DeMBA_{age}_segmentation_{year}.nii.gz"
        nib.save(out_img, out_filename)
