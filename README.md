# Project overview
 The DeMBA project aims to create 3D atlases of the postnatal mouse brain that are compatible with the Allen Mouse brain Common Coordinate Framework (Allen CCF) delineations.
 To do this, we perform 3D-to-3D registration of the Allen CCF template to templates of developing mouse brains (P7, P14, P21 and P28) acquired by serial two photon microscopy and published by [Newmaster and colleagues](https://www.nature.com/articles/s41467-020-15659-1).
 The deformation of the templates is subsequently used to transform the delineations in the same way, providing Allen CCF delineations in the template space for each age group.

# Data availability
 The templates used in the transformation and the resulting atlases are shared via the EBRAINS Knowledge Graph.

 ### DeMBA templates
 The templates were originally acquired and shared by [Newmaster and colleagues](https://www.nature.com/articles/s41467-020-15659-1) as .tif files with a (20 * 20 * 50 µm) voxel resolution. We converted these to .nii files, resampled them to isotropic (20 * 20 * 20 µm) voxel resolution, and re-oriented to RAS format. The resulting resampled and reoriented templates were used in the transformations and are shared under the following datasets:
- Kleven H, Qu H, Carey H, Leergaard TB & Bjerke IE (2023). Population-averaged 3D isotropic serial two-photon tomography reference data for the P7 mouse brain (v1). EBRAINS. [https://doi.org/10.25493/6Q3B-Q1U](https://doi.org/10.25493/6Q3B-Q1U)
- Kleven H, Qu H, Carey H, Leergaard TB & Bjerke IE (2023). Population-averaged 3D isotropic serial two-photon tomography reference data for the P14 mouse brain (v1). EBRAINS. [https://doi.org/10.25493/A6Z4-KPW](https://doi.org/10.25493/A6Z4-KPW)
- Kleven H, Qu H, Carey H, Leergaard TB & Bjerke IE (2023). Population-averaged 3D isotropic serial two-photon tomography reference data for the P21 mouse brain (v1). EBRAINS. [https://doi.org/10.25493/SJ4J-YAG](https://doi.org/10.25493/SJ4J-YAG)
- Kleven H, Qu H, Carey H, Leergaard TB & Bjerke IE (2023). Population-averaged 3D isotropic serial two-photon tomography reference data for the P28 mouse brain (v1). EBRAINS. [https://doi.org/10.25493/GQCH-G31](https://doi.org/10.25493/GQCH-G31)


### DeMBA annotation sets
 The Allen CCF delineations (2017 and 2022 versions) were transformed to fit the DeMBA templates, and the resulting delineation volumes are shared under the following datasets:
- ...

 # Code
 This repository contains all the code used in the DeMBA project. The scripts are sorted into four main folders:

 ## volume_preprocessing_pipeline
 - **download_original_allen_data.py** This script can be used to download the template and label files from the Allen Institute used in the current project.
 - **reorient_original_allen_data.py** This scripts reorients the Allen data to be in the same orientation as the DeMBA volumes, which is crucial for the use of corresponding points in the registration.
 - **download_reoriented_dev_templates.py** This script can be used to dowload the DeMBA templates from the EBRAINS Knowledge Graph.
 - 
 ## elastix_transformation
 - **DeMBA_functions.py** This script contains the functions used for elastix transformation.
 - **DeMBA_runs.py** This script was used to run transformations in the project. It allows you to run transformations specified fixed and moving volumes and copies all resulting files to a unique run directory, making it easy to keep an overview of different runs and results.

 ## volume_interpolation
   
 ## other
 The scripts in this folder are not part of the preprocessing or transformation pipeline but might be useful when working with volumes:
 - **make_thumbnail_flythrough.py** This script creates a flythrough video of a volume file, suitable for use as a preview image on the EBRAINS Knowledge Graph.
 - **label_annotationIDs_sequential.py** This script converts all the IDs in the Allen annotation volumes to sequential IDs. This avoids rounding errors for large IDs when using elastix.
 - **relabel_annotationIDs_Allen.py** This script converts all the sequential IDs back to IDs from the Allen Institute ontology.

 # Useful tips
 - We use the SimpleITK package for elastix. Be aware that there is another package called simpleITK. To make sure you import the right package, first pip install SimpleITK-SimpleElastix.
