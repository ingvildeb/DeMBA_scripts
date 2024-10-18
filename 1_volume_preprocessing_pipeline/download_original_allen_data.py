import os
import requests

"""
The following files are downloaded from the Allen Institute and need to be reoriented for our workflow
"""
if not os.path.exists("original_data"):
    os.makedirs("original_data")
allen_basepath_url = (
    r"https://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf"
)
# Define the original data URLs
template_url = rf"{allen_basepath_url}/average_template/average_template_10.nrrd"
annotation_2017_url = rf"{allen_basepath_url}/annotation/ccf_2017/annotation_10.nrrd"
annotation_2022_url = rf"{allen_basepath_url}/annotation/ccf_2022/annotation_10.nrrd"
# Define the save paths
template_path = r"original_data/average_template_10.nrrd"
annotation_2017_path = r"original_data/annotation_10_2017.nrrd"
annotation_2022_path = r"original_data/annotation_10_2022.nrrd"
# Download the files
print("Downloading the template...")
r = requests.get(template_url, allow_redirects=True, verify=False)
open(template_path, "wb").write(r.content)
print("Downloading the 2017 annotation...")
r = requests.get(annotation_2017_url, allow_redirects=True, verify=False)
open(annotation_2017_path, "wb").write(r.content)
print("Downloading the 2022 annotation...")
r = requests.get(annotation_2022_url, allow_redirects=True, verify=False)
open(annotation_2022_path, "wb").write(r.content)
