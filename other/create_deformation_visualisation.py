import CCF_translator
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from tqdm import tqdm
import inspect
import os
from scipy.interpolate import griddata
from scipy.ndimage import generic_filter

# Get the file path of the package
package_path = inspect.getfile(CCF_translator)

# Get the directory of the package
package_dir = os.path.dirname(package_path)





data_dir = r"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/demba_dev_mouse"
key_ages = [56, 28, 21, 14, 7, 4]



def interpolate_nans(data):
    x, y = np.indices(data.shape)
    valid_mask = ~np.isnan(data)
    coords = np.array([x[valid_mask], y[valid_mask]]).T
    values = data[valid_mask]
    
    # Initial linear interpolation
    interpolated = griddata(coords, values, (x, y), method='linear')
    
    # Handle any remaining NaNs with nearest-neighbor interpolation
    remaining_nans = np.isnan(interpolated)
    if np.any(remaining_nans):
        interpolated[remaining_nans] = griddata(coords, values, (x, y), method='nearest')[remaining_nans]
    
    return interpolated

age = key_ages[0]


template_dir = r"/home/harryc/github/DeMBA_scripts/data_files/allen_stpt_10um/"
template_vol_path = f"{template_dir}/DeMBA_P{age}_AllenSTPT_10um.nii.gz"
template_img = nib.load(template_vol_path)
template_arr = template_img.get_fdata()
dim1 = template_arr.shape[1]
dim2 = template_arr.shape[2]

# Create a regular grid
grid_spacing = 61.42215  # Adjust the spacing as needed

x, y = np.meshgrid(np.linspace(0, dim2, int(dim2 / grid_spacing) + 1), 
                   np.linspace(0, dim1, int(dim1 / grid_spacing) + 1))

# Create a figure with a higher resolution
plt.figure(figsize=(10, 10), dpi=300)

# Plot the image
plt.imshow(template_arr[600, :, :], cmap='gray')

# Plot the deformed grid
for i in range(y.shape[0]):
    plt.plot(x[i, :], y[i, :], color='red', linewidth=1)
for j in range(x.shape[1]):
    plt.plot(x[:, j], y[:, j], color='red', linewidth=1)

# plt.title("Deformation Field Visualization")
plt.axis('off')
plt.tight_layout()

# Save the plot as an SVG file with higher resolution
plt.savefig(f"../data_files/deformation_field_P{age}.svg", format="svg", dpi=300)

plt.show()
slice_index = 600

for i in tqdm(range(len(key_ages) - 1)):
    above_age = key_ages[i]
    age = key_ages[ i + 1]
    mag = key_ages[i] - age
    template_vol_path = f"{template_dir}/DeMBA_P{age}_AllenSTPT_10um.nii.gz"
    template_img = nib.load(template_vol_path)
    template_arr = template_img.get_fdata()
    base_path = r"/home/harryc/github/CCF_translator/CCF_translator/"
    metadata_path = rf"{package_dir}/metadata/translation_metadata.csv"
    metadata = pd.read_csv(metadata_path)
    source = f"demba_dev_mouse_P{age}"
    target = "demba_dev_mouse_P56"
    deform_arr = nib.load(f"{base_path}/metadata/deformation_fields/demba_dev_mouse/{above_age}_pull_{above_age - 1}.nii.gz").get_fdata()
    deform_arr *= mag
    ###############################
    # Extract the deformation vectors for the 2D slice
    deformation_x = deform_arr[slice_index // 2, :, :, 1].copy()
    deformation_y = deform_arr[slice_index // 2, :, :, 2].copy()
    
    deformation_x *= -1
    deformation_y *= -1

    # Create a regular grid
    grid_spacing = 62.52215  # Adjust the spacing as needed
    x, y = np.meshgrid(np.linspace(0, dim2, int(dim2 / grid_spacing) + 1), 
                    np.linspace(0, dim1, int(dim1 / grid_spacing) + 1))
                    
    grid_spacing = np.round(grid_spacing / 2 ).astype(int)
    # Apply the deformation to the grid points
    dx = deformation_x[::grid_spacing, ::grid_spacing ]
    dy = deformation_y[::grid_spacing , ::grid_spacing ]

    # Interpolate the NaN values
    if np.isnan(dx).any():
        dx = interpolate_nans(dx)
    if np.isnan(dy).any():
        dy = interpolate_nans(dy)
    deformed_x = x + dx
    deformed_y = y + dy
    
    plt.figure(figsize=(10, 10), dpi=300)
    
    # Plot the image
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.imshow(template_arr[600, :, :], cmap='gray')

    # Plot the deformed grid
    for i in range(y.shape[0]):
        ax.plot(deformed_x[i, :], deformed_y[i, :], color='red', linewidth=1)
    for j in range(x.shape[1]):
        ax.plot(deformed_x[:, j], deformed_y[:, j], color='red', linewidth=1)

    # plt.title("Deformation Field Visualization")
    ax.axis('off')
    plt.tight_layout()
    # Create a figure with a higher resolution

    # Save the plot as an SVG file with higher resolution
    plt.savefig(f"../data_files/deformation_field_P{age}.svg", format="svg", dpi=300, facecolor=fig.get_facecolor())
    plt.show()



age = key_ages[-1]


template_dir = r"/home/harryc/github/DeMBA_scripts/data_files/allen_stpt_10um/"
template_vol_path = f"{template_dir}/DeMBA_P{age}_AllenSTPT_10um.nii.gz"
template_img = nib.load(template_vol_path)
template_arr = template_img.get_fdata()
dim1 = template_arr.shape[1]
dim2 = template_arr.shape[2]

# Create a regular grid
grid_spacing = 61.42215  # Adjust the spacing as needed

x, y = np.meshgrid(np.linspace(0, dim2, int(dim2 / grid_spacing) + 1), 
                   np.linspace(0, dim1, int(dim1 / grid_spacing) + 1))

# Create a figure with a higher resolution
plt.figure(figsize=(10, 10), dpi=300)

# Plot the image
plt.imshow(template_arr[600, :, :], cmap='gray')

# Plot the deformed grid
for i in range(y.shape[0]):
    plt.plot(x[i, :], y[i, :], color='red', linewidth=1)
for j in range(x.shape[1]):
    plt.plot(x[:, j], y[:, j], color='red', linewidth=1)

# plt.title("Deformation Field Visualization")
plt.axis('off')
plt.tight_layout()

# Save the plot as an SVG file with higher resolution
plt.savefig(f"../data_files/reverse_deformation_field_P{age}.svg", format="svg", dpi=300)

plt.show()

for i in tqdm(range(len(key_ages) - 1)):
    index = len(key_ages) - i - 1
    above_age = key_ages[index]
    age = key_ages[ index - 1]
    mag = above_age - age
    template_vol_path = f"{template_dir}/DeMBA_P{age}_AllenSTPT_10um.nii.gz"
    template_img = nib.load(template_vol_path)
    template_arr = template_img.get_fdata()
    base_path = r"/home/harryc/github/CCF_translator/CCF_translator/"
    metadata_path = rf"{package_dir}/metadata/translation_metadata.csv"
    metadata = pd.read_csv(metadata_path)
    source = f"demba_dev_mouse_P{age}"
    target = "demba_dev_mouse_P56"
    deform_arr = nib.load(f"{base_path}/metadata/deformation_fields/demba_dev_mouse/{above_age}_pull_{above_age + 1}.nii.gz").get_fdata()
    deform_arr *= mag
    ###############################
    # Extract the deformation vectors for the 2D slice
    deformation_x = deform_arr[slice_index // 2, :, :, 1].copy()
    deformation_y = deform_arr[slice_index // 2, :, :, 2].copy()
    
    deformation_x *= 1
    deformation_y *= 1

    # Create a regular grid
    grid_spacing = 62.52215  # Adjust the spacing as needed
    x, y = np.meshgrid(np.linspace(0, dim2, int(dim2 / grid_spacing) + 1), 
                    np.linspace(0, dim1, int(dim1 / grid_spacing) + 1))
                    
    grid_spacing = np.round(grid_spacing / 2 ).astype(int)
    # Apply the deformation to the grid points
    dx = deformation_x[::grid_spacing, ::grid_spacing ]
    dy = deformation_y[::grid_spacing , ::grid_spacing ]

    # Interpolate the NaN values
    if np.isnan(dx).any():
        dx = interpolate_nans(dx)
    if np.isnan(dy).any():
        dy = interpolate_nans(dy)
    deformed_x = x + dx
    deformed_y = y + dy
    
    plt.figure(figsize=(10, 10), dpi=300)
    
    # Plot the image
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.imshow(template_arr[600, :, :], cmap='gray')

    # Plot the deformed grid
    for i in range(y.shape[0]):
        ax.plot(deformed_x[i, :], deformed_y[i, :], color='red', linewidth=1)
    for j in range(x.shape[1]):
        ax.plot(deformed_x[:, j], deformed_y[:, j], color='red', linewidth=1)

    # plt.title("Deformation Field Visualization")
    ax.axis('off')
    plt.tight_layout()
    # Create a figure with a higher resolution
    # Save the plot as an SVG file with higher resolution
    plt.savefig(f"../data_files/reverse_deformation_field_P{age}.svg", format="svg", dpi=300, facecolor=fig.get_facecolor())
    plt.show()
    