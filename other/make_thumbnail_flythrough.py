import cv2
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
# Load the nii volume
nii_files = [
    'DeMBA_P7_brain.nii',
    'DeMBA_P14_brain.nii',
    'DeMBA_P21_brain.nii',
    'DeMBA_P28_brain.nii.gz'
]
import numpy as np

def pad_to_square(arr):
    """
    Pads a given array to be square by adding zeros to the right and bottom edges.
    """
    rows = len(arr)
    cols = len(arr[0])
    max_dim = max(rows, cols)
    row_pad = (max_dim - rows) // 2
    col_pad = (max_dim - cols) // 2
    padded_arr = np.pad(arr, ((row_pad, row_pad), (col_pad, col_pad)), 'edge')
    return padded_arr


for nii_file in nii_files[:]:
    nii_img = nib.load(nii_file)
    data = nii_img.get_fdata()
    # change the order of the axes
    data = np.transpose(data, (2,0,1))
    # flip two of the axes
    data = data[:, ::-1, ::-1]
    nii_data = data.copy()
    # Normalize the data and clip the outlier frames
    min_val = np.percentile(nii_data, 1)
    max_val = np.percentile(nii_data, 99.9)
    nii_data = np.clip(nii_data, min_val, max_val)
    nii_data = (nii_data - min_val) / (max_val - min_val) * 255
    nii_data = nii_data.astype(np.uint8)
    output_res = (250, 250)

    # Define the number of frames per second for the output video
    fps = 30

    output_file = nii_file.split('.')[0] + '_thumbnail.mp4'


    # Create a VideoWriter object to write the output video
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(output_file, fourcc, fps, output_res)
    thumbnail_image = np.rot90(nii_data[350, :, :])
    thumbnail_image = pad_to_square(thumbnail_image)
    thumbnail_image = cv2.resize(thumbnail_image, output_res)
    # save the thumbnail image
    cv2.imwrite(nii_file.split('.')[0] + '_thumbnail.png', thumbnail_image)
    # Create a loop to iterate through each plane
    for plane in range(3):
        # Create a loop to iterate through each slice in the plane
        for slice_idx in range(nii_data.shape[plane]):
            # Extract the 2D image data and resize it to the desired resolution
            if plane == 0:
                img_data = np.rot90(nii_data[slice_idx, :, :])
            elif plane == 1:
                img_data = np.rot90(nii_data[:, slice_idx, :])
            else:
                img_data = np.rot90(nii_data[:, :, slice_idx])
            img_data = pad_to_square(img_data)
            img_data = cv2.resize(img_data, output_res)
            # Write the resized image data to the output video file
            out.write(cv2.cvtColor(img_data, cv2.COLOR_GRAY2BGR))

    # Release the VideoWriter object and close the output video file
    out.release()