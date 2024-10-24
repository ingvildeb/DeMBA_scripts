import pandas as pd
import nibabel as nib
import numpy as np

np.set_printoptions(suppress=True)  # prevent numpy exponential
colours = {
    "Isocortex": "#3F631C",
    "Hippocampal formation": "#7ED04B",
    "Olfactory areas": "#9AD2BD",
    "Hypothalamus": "#E32F21",
    "Cerebral nuclei": "#98D6F9",
    "Midbrain, hindbrain, medulla": "#FF9B88",
    "Thalamus": "#FF70A4",
    "Cerebellum": "#F0F080",
    "Fibre Tracts": "#CCCCCC",
    "Ventricular System": "#AAAAAA",
}
new_names = {
    "Cortex": "Isocortex",
    "Hippo": "Hippocampal formation",
    "Olfactory": "Olfactory areas",
    "Hypothalamus": "Hypothalamus",
    "Striatum_Pallidum": "Cerebral nuclei",
    "Mid_Hind_Medulla": "Midbrain, hindbrain, medulla",
    "Thalamus": "Thalamus",
    "Cerebellum": "Cerebellum",
    "Fibretracts": "Fibre Tracts",
    "VentricularSystem": "Ventricular System",
}


colour_lookup = pd.read_excel(
    r"/home/harryc/github/DeMBA_scripts/data_files/CustomRegionMouse_2017.xlsx"
)
colour_lookup = colour_lookup.rename(columns=new_names)

arr = nib.load(
    "/home/harryc/github/CCF_translator_local/demo_data/demba_20um/P56_annotation_20um.nii.gz"
).get_fdata()
df = pd.read_excel(
    r"/home/harryc/github/DeMBA_scripts/data_files/DeMBA_landmarksValidation_Ingvild.xlsx"
)


region_graph_colour = {
    i: j
    for i, j in zip(
        df["Acronym"].values,
        arr[
            df["adult: x (sagittal sections)"].tolist(),
            df["adult: y (horizontal sections)"].tolist(),
            df["adult: z (coronal sections)"].tolist(),
        ],
    )
}


point_lookup = {"point name": [], "hierarchical_region": []}

for point_name, v in region_graph_colour.items():
    hierarchical_region = "unknown"
    if v == 0:
        hierarchical_region = "out of brain"

    else:
        for r in colour_lookup.columns[1:]:
            temp_ids = colour_lookup[r].iloc[2:]
            if v in temp_ids.values.astype(float):
                hierarchical_region = r

    point_lookup["hierarchical_region"].append(hierarchical_region)
    point_lookup["point name"].append(point_name)


point_df = pd.DataFrame(point_lookup)
point_df.to_csv(r"../data_files/points_hierarchies.csv")
