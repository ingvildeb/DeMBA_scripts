import os
import numpy as np
from CCF_translator.deformation import apply_deformation, route_calculation
import CCF_translator
import pandas as pd
from tqdm import tqdm

key_ages = [56, 28, 21, 14, 7, 4]
points_dataset_h = pd.read_excel(r"../data_files/DeMBA_landmarksValidation_Heidi.xlsx")
points_dataset_i = pd.read_excel(
    r"../data_files/DeMBA_landmarksValidation_Ingvild.xlsx"
)
points_dataset_s = pd.read_excel(r"../data_files/DeMBA_landmarksValidation_Simon.xlsx")
points_dataset_r = pd.read_excel(
    r"../data_files/DeMBA_landmarksValidation_Harry.xlsx"
)  # Harry's data

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


for m in ["iterative"]:  # , "individual"]:
    mean_older_points = None
    for i in tqdm(range(len(key_ages) - 1)):
        older_age = key_ages[i]
        if older_age == 56:
            name_older_age = "adult"
        else:
            name_older_age = f"P{str(older_age).zfill(2)}"

        younger_age = key_ages[i + 1]

        name_younger_age = f"P{str(younger_age).zfill(2)}"
        older_points_heidi = extract_points_from_df(points_dataset_h, name_older_age)
        younger_points_heidi = extract_points_from_df(
            points_dataset_h, name_younger_age
        )
        older_points_ingvild = extract_points_from_df(points_dataset_i, name_older_age)
        younger_points_ingvild = extract_points_from_df(
            points_dataset_i, name_younger_age
        )
        older_points_simon = extract_points_from_df(points_dataset_s, name_older_age)
        younger_points_simon = extract_points_from_df(
            points_dataset_s, name_younger_age
        )
        older_points_harry = extract_points_from_df(
            points_dataset_r, name_older_age
        )  # Extract older points for Harry
        younger_points_harry = extract_points_from_df(
            points_dataset_r, name_younger_age
        )  # Extract younger points for Harry

        if mean_older_points is None or m == "individual":
            mean_older_points = np.mean(
                [
                    older_points_ingvild,
                    older_points_heidi,
                    older_points_simon,
                    older_points_harry,
                ],
                axis=0,
            )
        points = CCF_translator.PointSet(
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
            if np.isnan(mean_older_points[i]).any():
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
            heidi_point = younger_points_heidi[i]
            ingvild_point = younger_points_ingvild[i]
            simon_point = younger_points_simon[i]
            harry_point = younger_points_harry[i]

            h_dist = one_vs_rest(heidi_point, [simon_point, ingvild_point, harry_point])
            s_dist = one_vs_rest(simon_point, [heidi_point, ingvild_point, harry_point])
            i_dist = one_vs_rest(ingvild_point, [simon_point, heidi_point, harry_point])
            r_dist = one_vs_rest(harry_point, [simon_point, heidi_point, ingvild_point])
            d1_dist = one_vs_rest(pred_point, [simon_point, ingvild_point, harry_point])
            d2_dist = one_vs_rest(pred_point, [heidi_point, ingvild_point, harry_point])
            d3_dist = one_vs_rest(pred_point, [heidi_point, simon_point, harry_point])
            # i want to make sure im comparing averages formed from only 2 individiuals
            d_dist = np.mean([d1_dist, d3_dist, d3_dist])
            h_i_dist = abs(np.linalg.norm(heidi_point - ingvild_point))
            d_i_dist = abs(np.linalg.norm(pred_point - ingvild_point))
            d_h_dist = abs(np.linalg.norm(pred_point - heidi_point))
            s_i_dist = abs(np.linalg.norm(simon_point - ingvild_point))
            s_h_dist = abs(np.linalg.norm(simon_point - heidi_point))
            s_d_dist = abs(np.linalg.norm(simon_point - pred_point))
            s_r_dist = abs(np.linalg.norm(simon_point - harry_point))
            r_h_dist = abs(np.linalg.norm(harry_point - heidi_point))
            r_i_dist = abs(np.linalg.norm(harry_point - ingvild_point))
            r_d_dist = abs(np.linalg.norm(harry_point - pred_point))

            ing.append(i_dist)
            sim.append(s_dist)
            hei.append(h_dist)
            dem.append(d_dist)
            har.append(r_dist)
            i2h.append(h_i_dist)
            h2d.append(d_h_dist)
            i2d.append(d_i_dist)
            s2i.append(s_i_dist)
            s2d.append(s_d_dist)
            s2h.append(s_h_dist)
            s2r.append(s_r_dist)
            r2h.append(r_h_dist)
            r2i.append(r_i_dist)
            r2d.append(r_d_dist)
            # Append coordinates

            hx.append(heidi_point[0])
            hy.append(heidi_point[1])
            hz.append(heidi_point[2])
            ix.append(ingvild_point[0])
            iy.append(ingvild_point[1])
            iz.append(ingvild_point[2])
            dx.append(pred_point[0])
            dy.append(pred_point[1])
            dz.append(pred_point[2])
            sx.append(simon_point[0])
            sy.append(simon_point[1])
            sz.append(simon_point[2])
            rx.append(harry_point[0])
            ry.append(harry_point[1])
            rz.append(harry_point[2])

        output_data = {
            "Acronym": points_dataset_h["Acronym"],
            "Full Name": points_dataset_h["Full name"],
            "Distance Ingvild to others": ing,
            "Distance Heidi to others": hei,
            "Distance Simon to others": sim,
            "Distance DeMBA to others": dem,
            "Distance Harry to others": har,
            "Distance Ingvild to Heidi": i2h,
            "Distance Ingvild to Demba": i2d,
            "Distance Heidi to Demba": h2d,
            "Distance Simon to Heidi": s2h,
            "Distance Simon to Demba": s2d,
            "Distance Simon to Ingvild": s2i,
            "Distance Simon to Harry": s2r,
            "Distance Harry to Heidi": r2h,
            "Distance Harry to Demba": r2d,
            "Distance Harry to Ingvild": r2i,
            "Heidi x": hx,
            "Heidi y": hy,
            "Heidi z": hz,
            "Ingvild x": ix,
            "Ingvild y": iy,
            "Ingvild z": iz,
            "Demba x": dx,
            "Demba y": dy,
            "Demba z": dz,
            "Simon x": sx,
            "Simon y": sy,
            "Simon z": sz,
            "Harry x": rx,
            "Harry y": ry,
            "Harry z": rz,
        }
        pd.DataFrame(output_data).to_csv(f"../data_files/{m}_{name_younger_age}.csv")
        mean_older_points = np.array(new_mean_older_points)

        print(f"ingvild distance: {np.nanmedian(ing)}")
        print(f"Simon distance: {np.nanmedian(sim)}")
        print(f"Heidi distance: {np.nanmedian(hei)}")
        print(f"DeMBA distance: {np.nanmedian(dem)}")
        print(f"Harry distance: {np.nanmedian(har)}")
