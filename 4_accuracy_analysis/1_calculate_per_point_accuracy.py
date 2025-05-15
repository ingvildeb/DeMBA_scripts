import os
import numpy as np
from brainglobe_ccf_translator.deformation import apply_deformation, route_calculation
import brainglobe_ccf_translator
import pandas as pd
from tqdm import tqdm
import scipy

key_ages = [56, 28, 21, 14, 7, 4]
points_dataset_rat3 = pd.read_excel(r"../data_files/DeMBA_landmarksValidation_Rater_3.xlsx")
points_dataset_rat1 = pd.read_excel(
    r"../data_files/DeMBA_landmarksValidation_Rater_1.xlsx"
)
points_dataset_rat2 = pd.read_excel(r"../data_files/DeMBA_landmarksValidation_Rater_2.xlsx")
points_dataset_rat4 = pd.read_excel(
    r"../data_files/DeMBA_landmarksValidation_Rater_3.xlsx"
)  # rater_4's data

keep_names = points_dataset_rat4["Full name"][points_dataset_rat4["Remove"] != 1]

points_dataset_rat3 = points_dataset_rat3[points_dataset_rat3["Full name"].isin(keep_names)]
points_dataset_rat1 = points_dataset_rat1[points_dataset_rat1["Full name"].isin(keep_names)]
points_dataset_rat2 = points_dataset_rat2[points_dataset_rat2["Full name"].isin(keep_names)]
points_dataset_rat4 = points_dataset_rat4[points_dataset_rat4["Full name"].isin(keep_names)]


target_space = "demba_dev_mouse"

col_format = "{}: {} ({} sections)"


def format_column_name(age_name, axis):
    axis_mapping = {"x": "sagittal", "y": "horizontal", "z": "coronal"}
    axis_name = axis_mapping.get(axis, "unknown")
    return f"{age_name}: {axis} ({axis_name} sections)"


def extract_points_from_df(dataset, age_name):
    return dataset[
        [
            format_column_name(age_name, "x"),
            format_column_name(age_name, "y"),
            format_column_name(age_name, "z"),
        ]
    ].values


def one_vs_rest(one_point, rest):
    rest_point = np.median(rest, axis=0)
    return abs(np.linalg.norm(rest_point - one_point))


mean_older_points = extract_points_from_df(points_dataset_rat3, "adult")
for m in ["iterative"]:  # , "individual"]:
    for i in tqdm(range(len(key_ages) - 1)):

        older_age = key_ages[i]

        younger_age = key_ages[i + 1]

        name_younger_age = f"P{str(younger_age).zfill(2)}"
        younger_points_rater_3 = extract_points_from_df(
            points_dataset_rat3, name_younger_age
        )
        younger_points_rater_1 = extract_points_from_df(
            points_dataset_rat1, name_younger_age
        )
        younger_points_rater_2 = extract_points_from_df(
            points_dataset_rat2, name_younger_age
        )
        younger_points_rater_4 = extract_points_from_df(
            points_dataset_rat4, name_younger_age
        )  # Extract younger points for rater_4
        # If any of the raters have placed the point outside the brain remove that point from the analysis
        top_mask_x = (
            (younger_points_rater_4[:, 0] < 570)
            & (younger_points_rater_1[:, 0] < 570)
            & (younger_points_rater_2[:, 0] < 570)
            & (younger_points_rater_3[:, 0] < 570)
        )
        top_mask_y = (
            (younger_points_rater_4[:, 1] < 400)
            & (younger_points_rater_1[:, 1] < 400)
            & (younger_points_rater_2[:, 1] < 400)
            & (younger_points_rater_3[:, 1] < 400)
        )
        top_mask_z = (
            (younger_points_rater_4[:, 2] < 705)
            & (younger_points_rater_1[:, 2] < 705)
            & (younger_points_rater_2[:, 2] < 705)
            & (younger_points_rater_3[:, 2] < 705)
        )
        bottom_mask = (
            (younger_points_rater_4 > 0)
            & (younger_points_rater_1 > 0)
            & (younger_points_rater_2 > 0)
            & (younger_points_rater_3 > 0)
        )
        mask = np.array((top_mask_x, top_mask_y, top_mask_z)).T & bottom_mask

        points = brainglobe_ccf_translator.PointSet(
            values=mean_older_points,
            space=target_space,
            age_PND=older_age,
            voxel_size_micron=20,
        )
        points.transform(target_age=younger_age, target_space=target_space)
        ing, sim, hei, dem, har = [], [], [], [], []
        s2i, s2d, s2h, i2h, i2d, h2d, s2r, r2h, r2i, r2d = (
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        )
        hx, hy, hz, ix, iy, iz, dx, dy, dz, sx, sy, sz, rx, ry, rz = (
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        )
        new_mean_older_points = []
        for i in range(len(mean_older_points)):
            if np.isnan(mean_older_points[i]).any() or not mask[i].all():
                new_mean_older_points.append([np.nan, np.nan, np.nan])
                i2h.append(np.nan)
                h2d.append(np.nan)
                i2d.append(np.nan)
                s2i.append(np.nan)
                s2d.append(np.nan)
                s2h.append(np.nan)
                s2r.append(np.nan)
                r2h.append(np.nan)
                r2i.append(np.nan)
                r2d.append(np.nan)
                hx.append(np.nan)
                hy.append(np.nan)
                hz.append(np.nan)
                ix.append(np.nan)
                iy.append(np.nan)
                iz.append(np.nan)
                dx.append(np.nan)
                dy.append(np.nan)
                dz.append(np.nan)
                sx.append(np.nan)
                sy.append(np.nan)
                sz.append(np.nan)
                rx.append(np.nan)
                ry.append(np.nan)
                rz.append(np.nan)
                ing.append(np.nan)
                sim.append(np.nan)
                hei.append(np.nan)
                dem.append(np.nan)
                har.append(np.nan)
                continue
            pred_point = points.values[i]
            new_mean_older_points.append(pred_point)
            rater_3_point = younger_points_rater_3[i]
            rater_1_point = younger_points_rater_1[i]
            rater_2_point = younger_points_rater_2[i]
            rater_4_point = younger_points_rater_4[i]

            h_dist = one_vs_rest(rater_3_point, [rater_2_point, rater_1_point, rater_4_point])
            s_dist = one_vs_rest(rater_2_point, [rater_3_point, rater_1_point, rater_4_point])
            i_dist = one_vs_rest(rater_1_point, [rater_2_point, rater_3_point, rater_4_point])
            r_dist = one_vs_rest(rater_4_point, [rater_2_point, rater_3_point, rater_1_point])
            d1_dist = one_vs_rest(pred_point, [rater_2_point, rater_1_point, rater_4_point])
            d2_dist = one_vs_rest(pred_point, [rater_3_point, rater_1_point, rater_4_point])
            d3_dist = one_vs_rest(pred_point, [rater_3_point, rater_2_point, rater_4_point])
            # i want to make sure im comparing averages formed from only 2 individiuals
            d_dist = np.mean([d1_dist, d3_dist, d3_dist])

            ing.append(i_dist)
            sim.append(s_dist)
            hei.append(h_dist)
            dem.append(d_dist)
            har.append(r_dist)

            # Append coordinates

            hx.append(rater_3_point[0])
            hy.append(rater_3_point[1])
            hz.append(rater_3_point[2])
            ix.append(rater_1_point[0])
            iy.append(rater_1_point[1])
            iz.append(rater_1_point[2])
            dx.append(pred_point[0])
            dy.append(pred_point[1])
            dz.append(pred_point[2])
            sx.append(rater_2_point[0])
            sy.append(rater_2_point[1])
            sz.append(rater_2_point[2])
            rx.append(rater_4_point[0])
            ry.append(rater_4_point[1])
            rz.append(rater_4_point[2])
        output_data = {
            "Acronym": points_dataset_rat3["Acronym"],
            "Full Name": points_dataset_rat3["Full name"],
            "Distance rater_1 to others": ing,
            "Distance rater_3 to others": hei,
            "Distance rater_2 to others": sim,
            "Distance DeMBA to others": dem,
            "Distance rater_4 to others": har,
            "rater_3 x": hx,
            "rater_3 y": hy,
            "rater_3 z": hz,
            "rater_1 x": ix,
            "rater_1 y": iy,
            "rater_1 z": iz,
            "Demba x": dx,
            "Demba y": dy,
            "Demba z": dz,
            "rater_2 x": sx,
            "rater_2 y": sy,
            "rater_2 z": sz,
            "rater_4 x": rx,
            "rater_4 y": ry,
            "rater_4 z": rz,
        }
        pd.DataFrame(output_data).to_csv(f"../data_files/{m}_{name_younger_age}.csv")
        mean_older_points = np.array(new_mean_older_points)

        print(f"rater_1 distance median: {np.nanmedian(ing)}")
        print(f"rater_2 distance median: {np.nanmedian(sim)}")
        print(f"rater_3 distance median: {np.nanmedian(hei)}")
        print(f"DeMBA distance median: {np.nanmedian(dem)}")
        print(f"rater_4 distance median: {np.nanmedian(har)}")
        print(f"rater_1 distance mean: {np.nanmean(ing)}")
        print(f"rater_2 distance mean: {np.nanmean(sim)}")
        print(f"rater_3 distance mean: {np.nanmean(hei)}")
        print(f"DeMBA distance mean: {np.nanmean(dem)}")
        print(f"rater_4 distance mean: {np.nanmean(har)}")

        print(f"rater_1 distance max: {np.nanmax(ing)}")
        print(f"rater_2 distance max: {np.nanmax(sim)}")
        print(f"rater_3 distance max: {np.nanmax(hei)}")
        print(f"DeMBA distance max: {np.nanmax(dem)}")
        print(f"rater_4 distance max: {np.nanmax(har)}")
