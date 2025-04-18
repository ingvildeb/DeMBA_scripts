import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from CCF_translator.deformation.interpolation.NearestNDInterpolator import (
    NearestNDInterpolator,
)
import nibabel as nib


def interpolate_volume(volume, mask):
    # Get the shape of the volume
    shape = volume.shape
    # Create a grid of points in the volume
    grid = np.mgrid[0 : shape[0], 0 : shape[1], 0 : shape[2]]
    points = grid.reshape((3, -1)).T
    # Flatten the volume
    mask = mask.flatten()
    values = volume.flatten()
    nan_pos = np.isnan(values)
    interp_mask = ~nan_pos & mask
    # Create the interpolator
    interpolator = NearestNDInterpolator(points[interp_mask], values[interp_mask])
    # Interpolate the volume
    out_mask = nan_pos & mask
    values[out_mask] = interpolator(points[out_mask], k=3, weights="distance")
    # Reshape the interpolated volume to the original shape
    interpolated_volume = values.reshape(shape)
    return interpolated_volume


threshold = 70
volume_shape = (570, 400, 705)
key_ages = [28, 21, 14, 7, 4]


for age in key_ages:
<<<<<<< HEAD
    points = pd.read_csv(rf"demo_data/individual_P{age}.csv")
    annotation = nib.load(
        rf"/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/interpolated_segmentations/AllenCCFv3_segmentations/DeMBA_P{age}_segmentation_2022.nii.gz"
    )
=======
    points = pd.read_csv(rf"../data_files/iterative_P{str(age).zfill(2)}.csv")
    annotation = nib.load(rf"../data_files/DeMBA_P{age}_segmentation_2017_20um.nii.gz")
>>>>>>> 16323dcad2cc41bbc71670b663582cba666e86c9
    annotation_vol = np.asanyarray(annotation.dataobj)
    volume = np.zeros(volume_shape)
    volume[:] = np.nan
    mask = points[["Demba x", "Demba y", "Demba z"]].isna().any(axis=1)
    points = points[~mask]
    t_points = np.round(points[["Demba x", "Demba y", "Demba z"]]).astype(int).values
    #convert from voxels to microns
    demba_dist = points[
        ["Distance DeMBA to others"]
    ].values.flatten()
    demba_dist = demba_dist * 20
    volume[t_points[:, 0], t_points[:, 1], t_points[:, 2]] = demba_dist
    volume = interpolate_volume(volume, annotation_vol != 0)
    out_img = nib.Nifti1Image(volume, annotation.affine, annotation.header)
    nib.save(out_img, f"../data_files/demba_{age}_error_volume.nii.gz")


for age in key_ages:
    points = pd.read_csv(rf"../data_files/iterative_P{str(age).zfill(2)}.csv")
    annotation = nib.load(rf"../data_files/DeMBA_P{age}_segmentation_2017_20um.nii.gz")
    annotation_vol = np.asanyarray(annotation.dataobj)
    volume = np.zeros(volume_shape)
    volume[:] = np.nan
    mask = (
        points[
            [
                "Harry x",
                "Harry y",
                "Harry z",
                "Ingvild x",
                "Ingvild y",
                "Ingvild z",
                "Simon x",
                "Simon y",
                "Simon z",
                "Heidi x",
                "Heidi y",
                "Heidi z",
            ]
        ]
<<<<<<< HEAD
    ]
    mask = [
        (points["Heidi x"] > 0)
        & (points["Ingvild x"] > 0)
        & (points["Demba x"] > 0)
        & (points["Heidi x"] < volume_shape[0])
        & (points["Ingvild x"] < volume_shape[0])
        & (points["Demba x"] < volume_shape[0])
        & (points["Heidi y"] > 0)
        & (points["Ingvild y"] > 0)
        & (points["Demba y"] > 0)
        & (points["Heidi y"] < volume_shape[1])
        & (points["Ingvild y"] < volume_shape[1])
        & (points["Demba y"] < volume_shape[1])
        & (points["Heidi z"] > 0)
        & (points["Ingvild z"] > 0)
        & (points["Demba z"] > 0)
        & (points["Heidi z"] < volume_shape[2])
        & (points["Ingvild z"] < volume_shape[2])
        & (points["Demba z"] < volume_shape[2])
        & distances["Distance Ingvild to Heidi"]
        < threshold
    ]
    distances = distances[mask[0]]
    points = points[mask[0]]
    volume = np.zeros(volume_shape)
    volume[:] = np.nan
    t_points = np.round(points[["Demba x", "Demba y", "Demba z"]]).astype(int).values
    volume[t_points[:, 0], t_points[:, 1], t_points[:, 2]] = distances[
        ["Distance Ingvild to Demba", "Distance Heidi to Demba"]
    ].mean(axis=1)
    volume = interpolate_volume(volume, annotation_vol != 0)
    out_img = nib.Nifti1Image(volume, annotation.affine, annotation.header)
    nib.save(out_img, f"demo_data/demba_{age}_error_volume.nii.gz")
    break
for age in key_ages:
    points = pd.read_csv(rf"demo_data/individual_P{age}.csv")
    annotation = nib.load(
        rf"/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/DeMBA_v2/interpolated_segmentations/AllenCCFv3_segmentations/DeMBA_P{age}_segmentation_2022.nii.gz"
=======
        .isna()
        .any(axis=1)
>>>>>>> 16323dcad2cc41bbc71670b663582cba666e86c9
    )
    points = points[~mask]


    ha_x = points["Harry x"]
    ha_y = points["Harry y"]
    ha_z = points["Harry z"]
    he_x = points["Heidi x"]
    he_y = points["Heidi y"]
    he_z = points["Heidi z"]    
    si_x = points["Simon x"]
    si_y = points["Simon y"]
    si_z = points["Simon z"]    
    in_x = points["Ingvild x"]
    in_y = points["Ingvild y"]
    in_z = points["Ingvild z"]    

    mean_human = np.array(((ha_x, ha_y, ha_z),
                  (he_x, he_y, he_z),
                  (si_x, si_y, si_z),
                  (in_x, in_y, in_z))).mean(axis=0)
    t_points = np.round( mean_human ).astype(int).T

    # Extract the data
    Ing = points["Distance Ingvild to others"]
    Sim = points["Distance Simon to others"]
    Hei = points["Distance Heidi to others"]
    Har = points["Distance Harry to others"]
    mean_human = np.mean([Ing, Sim, Hei, Har], axis=0)
    #convert from voxels to microns
    mean_human = mean_human * 20
    volume[t_points[:, 0], t_points[:, 1], t_points[:, 2]] = mean_human.flatten()
    volume = interpolate_volume(volume, annotation_vol != 0)
    out_img = nib.Nifti1Image(volume, annotation.affine, annotation.header)
<<<<<<< HEAD
    nib.save(out_img, f"demo_data/heidi_ingvild_{age}_error_volume.nii.gz")
    
=======
    nib.save(out_img, f"../data_files/average_human_{age}_error_volume.nii.gz")
>>>>>>> 16323dcad2cc41bbc71670b663582cba666e86c9
