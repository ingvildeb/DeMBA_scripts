import CCF_translator
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from tqdm import tqdm
import inspect
import os

# Get the file path of the package
package_path = inspect.getfile(CCF_translator)

# Get the directory of the package
package_dir = os.path.dirname(package_path)





data_dir = r"/home/harryc/github/CCF_translator/CCF_translator/metadata/deformation_fields/demba_dev_mouse"
key_ages = [56, 28, 21, 14, 7, 4]







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
    age = key_ages[ i + 1]
    template_vol_path = f"{template_dir}/DeMBA_P{age}_AllenSTPT_10um.nii.gz"
    template_img = nib.load(template_vol_path)
    template_arr = template_img.get_fdata()
    base_path = r"/home/harryc/github/CCF_translator/CCF_translator/"
    metadata_path = rf"{package_dir}/metadata/translation_metadata.csv"
    metadata = pd.read_csv(metadata_path)
    G = CCF_translator.deformation.route_calculation.create_G(metadata)
    source = f"demba_dev_mouse_P{age}"
    target = "demba_dev_mouse_P56"
    route = CCF_translator.deformation.route_calculation.calculate_route(source, target, G)
    deform_arr, pad_sum, flip_sum, dim_order_sum, final_voxel_size = (
        CCF_translator.deformation.apply_deformation.combine_route(
            route, 20, base_path, metadata
        )
    )
    ###############################
    # Extract the deformation vectors for the 2D slice
    deformation_x = deform_arr[1, slice_index // 2, :, :].copy()
    deformation_y = deform_arr[2, slice_index // 2, :, :].copy()
    deformation_x *= 2
    deformation_y *= 2

    # Create a regular grid
    grid_spacing = 62.52215  # Adjust the spacing as needed
    x, y = np.meshgrid(np.linspace(0, dim2, int(dim2 / grid_spacing) + 1), 
                    np.linspace(0, dim1, int(dim1 / grid_spacing) + 1))
    grid_spacing = np.ceil(grid_spacing / 2 ).astype(int)
    # Apply the deformation to the grid points
    deformed_x =( x + deformation_x[::grid_spacing, ::grid_spacing ]) 
    deformed_y =( y + deformation_y[::grid_spacing , ::grid_spacing ])
    
    # Plot the image
    plt.imshow(template_arr[600, :, :], cmap='gray')

    # Plot the deformed grid
    for i in range(y.shape[0]):
        plt.plot(deformed_x[i, :], deformed_y[i, :], color='red', linewidth=1)
    for j in range(x.shape[1]):
        plt.plot(deformed_x[:, j], deformed_y[:, j], color='red', linewidth=1)

    # plt.title("Deformation Field Visualization")
    plt.axis('off')
    plt.tight_layout()

    # Save the plot as an SVG file with higher resolution
    plt.savefig(f"../data_files/deformation_field_P{age}.svg", format="svg", dpi=300)
    plt.show()
