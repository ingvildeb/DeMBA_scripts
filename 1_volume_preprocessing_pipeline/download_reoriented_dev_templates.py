import os
import requests

"""
The following files have already been reoriented for our workflow so we can save them in the reoriented_data folder
"""
if not os.path.exists("reoriented_data"):
    os.makedirs("reoriented_data")
ebrains_basepath_url = r"https://data-proxy.ebrains.eu/api/v1/buckets"
# Define the reoriented data URLs
p7_template_url = rf"{ebrains_basepath_url}/d-36241bd6-ff03-45da-b07f-2bd94065a898/DeMBA_P7_brain.nii?inline=true"
p14_template_url = rf"{ebrains_basepath_url}/d-d3e76e7a-7e43-431a-ae30-b15411970ba9/DeMBA_P14_brain.nii?inline=true"
p21_template_url = rf"{ebrains_basepath_url}/d-db967ce1-dd49-4ef3-8fa9-55aa50709ce4/DeMBA_P21_brain.nii?inline=true"
p28_template_url = rf"{ebrains_basepath_url}/d-4ef11fc0-0de8-4689-a3b1-40b09fdeffac/DeMBA_P28_brain.nii.gz?inline=true"
# Define the save paths
p7_template_path = r"reoriented_data/DeMBA_P7_brain.nii"
p14_template_path = r"reoriented_data/DeMBA_P14_brain.nii"
p21_template_path = r"reoriented_data/DeMBA_P21_brain.nii"
p28_template_path = r"reoriented_data/DeMBA_P28_brain.nii.gz"
# Download the files
print("Downloading the P7 template...")
r = requests.get(p7_template_url, allow_redirects=True, verify=False)
open(p7_template_path, "wb").write(r.content)
print("Downloading the P14 template...")
r = requests.get(p14_template_url, allow_redirects=True, verify=False)
open(p14_template_path, "wb").write(r.content)
print("Downloading the P21 template...")
r = requests.get(p21_template_url, allow_redirects=True, verify=False)
open(p21_template_path, "wb").write(r.content)
print("Downloading the P28 template...")
r = requests.get(p28_template_url, allow_redirects=True, verify=False)
open(p28_template_path, "wb").write(r.content)
