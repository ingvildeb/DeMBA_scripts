# Project overview
The Developmental Mouse Brain Atlas (DeMBA) is a four-dimensional atlas encompassing each postnatal day from 4 to 56, with delineations that are fully compatible with the Allen Mouse brain Common Coordinate Framework (Allen CCF) delineations. The atlas was created by 3D-to-3D registration of the Allen CCF template [(Wang and colleagues)](https://www.sciencedirect.com/science/article/pii/S0092867420304025?via%3Dihub) to templates of developing mouse brains (P4, P7, P14, P21 and P28) acquired by serial two photon microscopy and published by [Newmaster and colleagues](https://www.nature.com/articles/s41467-020-15659-1) and [Liwang and colleagues](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10690281/). The deformation of the templates is subsequently used to transform the delineations in the same way, providing Allen CCF delineations in the template space for each age group. The deformation matrices were further used to create interpolated models of what the template and segmentations would look like at intermediate ages. 

### :page_facing_up: **For more information about the atlas and how it can be used, read our [preprint](https://www.biorxiv.org/content/biorxiv/early/2024/06/14/2024.06.14.598876.full.pdf).**

# Data availability
 The templates used in the transformation and the resulting atlases are shared via the EBRAINS Knowledge Graph.

 ### DeMBA atlas with continuous coverage from P4-P56
 - Carey, H., Ovsthus, M., Kleven, H., Yates, S. C., Csucs, G., Puchades, M. A., Bjaalie, J. G., Leergaard, T. B., & Bjerke, I. E. (2024). Developmental mouse brain atlas (DeMBA) with continuous coverage of postnatal day 4 to 56 (v1) [Data set]. EBRAINS. https://doi.org/10.25493/PWDG-536

 ### DeMBA templates
 The P7, P14, P21 and P28 templates were originally acquired and shared by [Newmaster and colleagues](https://www.nature.com/articles/s41467-020-15659-1) as .tif files with a (20 * 20 * 50 µm) voxel resolution. We resampled them to isotropic (20 * 20 * 20 µm) voxel resolution. The P4 template was shared by [Liwang and colleagues](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10690281/) and was already provided in isotropic (20 * 20 * 20 µm) resolution. All the templates were re-oriented and processed to optimize them for co-registration. The processed templates, as used in our registration workflow, can be found under the following datasets:
- Carey, H., Kleven, H., Leergaard, T. B., & Bjerke, I. E. (2024). Population-averaged 3D isotropic serial two-photon tomography reference data for the P4 mouse brain (v1) [Data set]. EBRAINS. [https://doi.org/10.25493/VNF6-E92](https://doi.org/10.25493/VNF6-E92)
- Carey, H., Kleven, H., Qu, H., Leergaard, T. B., & Bjerke, I. E. (2024). Population-averaged 3D isotropic serial two-photon tomography reference data for the P7 mouse brain (v2) [Data set]. EBRAINS. [https://doi.org/10.25493/JKBM-608](https://doi.org/10.25493/JKBM-608)
- Carey, H., Kleven, H., Qu, H., Leergaard, T. B., & Bjerke, I. E. (2024). Population-averaged 3D isotropic serial two-photon tomography reference data for the P14 mouse brain (v2) [Data set]. EBRAINS. [https://doi.org/10.25493/KAHK-14](https://doi.org/10.25493/KAHK-14)
- Carey, H., Kleven, H., Qu, H., Leergaard, T. B., & Bjerke, I. E. (2024). Population-averaged 3D isotropic serial two-photon tomography reference data for the P21 mouse brain (v2) [Data set]. EBRAINS. [https://doi.org/10.25493/2FMJ-152](https://doi.org/10.25493/2FMJ-152)
- Carey, H., Kleven, H., Qu, H., Leergaard, T. B., & Bjerke, I. E. (2024). Population-averaged 3D isotropic serial two-photon tomography reference data for the P28 mouse brain (v2) [Data set]. EBRAINS. [https://doi.org/10.25493/TG8Z-PER](https://doi.org/10.25493/TG8Z-PER)

### DeMBA annotation sets
 The Allen CCF segmentations (2017 and 2022 versions) were transformed to fit the DeMBA templates, and the resulting segmentation volumes are shared under the following datasets:
- Carey, H., Ovsthus, M., Kleven, H., Leergaard, T. B., & Bjerke, I. E. (2024). Allen Mouse Brain CCFv3 segmentations transformed to P4 population-averaged serial two-photon tomography data (v1) [Data set]. EBRAINS. [https://doi.org/10.25493/QG9H-16Y](https://doi.org/10.25493/QG9H-16Y)
- Ovsthus, M., Carey, H., Kleven, H., Leergaard, T. B., & Bjerke, I. E. (2024). Allen Mouse Brain CCFv3 segmentations transformed to P7 population-averaged serial two-photon tomography data (v1) [Data set]. EBRAINS. [https://doi.org/10.25493/NAWP-ND2](https://doi.org/10.25493/NAWP-ND2)
- Ovsthus, M., Carey, H., Kleven, H., Leergaard, T. B., & Bjerke, I. E. (2024). Allen Mouse Brain CCFv3 segmentations transformed to P14 population-averaged serial two-photon tomography data (v1) [Data set]. EBRAINS. [https://doi.org/10.25493/SZSR-BFZ](https://doi.org/10.25493/SZSR-BFZ)
- Ovsthus, M., Carey, H., Kleven, H., Leergaard, T. B., & Bjerke, I. E. (2024). Allen Mouse Brain CCFv3 segmentations transformed to P21 population-averaged serial two-photon tomography data (v1) [Data set]. EBRAINS. [https://doi.org/10.25493/JZKH-XWK](https://doi.org/10.25493/JZKH-XWK)
- Ovsthus, M., Carey, H., Kleven, H., Leergaard, T. B., & Bjerke, I. E. (2024). Allen Mouse Brain CCFv3 segmentations transformed to P28 population-averaged serial two-photon tomography data (v1) [Data set]. EBRAINS. [https://doi.org/10.25493/GVT5-4K9](https://doi.org/10.25493/GVT5-4K9)


 # Code
 This repository contains all the code used for the 3D-to-3D registration underlying DeMBA. The scripts are sorted into three main folders:

 ### volume_preprocessing_pipeline
 - **download_original_allen_data.py** This script can be used to download the template and label files from the Allen Institute used in the current project.
 - **reorient_original_allen_data.py** This scripts reorients the Allen data to be in the same orientation as the DeMBA volumes, which is crucial for the use of corresponding points in the registration.
 - **download_reoriented_dev_templates.py** This script can be used to dowload the DeMBA templates from the EBRAINS Knowledge Graph.
   
 ### elastix_transformation
 - **DeMBA_functions.py** This script contains the functions used for elastix transformation.
 - **DeMBA_runs.py** This script was used to run transformations in the project. It allows you to run transformations specified fixed and moving volumes and copies all resulting files to a unique run directory, making it easy to keep an overview of different runs and results.
 - **DeMBA_P[X].py** These scripts (with X indicating the postnatal day of the fixed age for the transform) are the exact scripts used in our registration, to produce the datasets listed under "DeMBA annotation sets".
   
 ### other
 The scripts in this folder are not part of the preprocessing or transformation pipeline but might be useful when working with volumes:
 - **make_thumbnail_flythrough.py** This script creates a flythrough video of a volume file, suitable for use as a preview image on the EBRAINS Knowledge Graph.
 - **label_annotationIDs_sequential.py** This script converts all the IDs in the Allen annotation volumes to sequential IDs. This avoids rounding errors for large IDs when using elastix.
 - **relabel_annotationIDs_Allen.py** This script converts all the sequential IDs back to IDs from the Allen Institute ontology.

The code used to interpolate the templates and segmentation to intermediate ages will be shared shortly.

 # Useful tips
 - We use the SimpleITK package for elastix. Be aware that there is another package called simpleITK. To make sure you import the right package, first pip install SimpleITK-SimpleElastix.
