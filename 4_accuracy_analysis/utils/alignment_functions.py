import ants
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import scipy
import imageio
from skimage.color import rgb2gray
from scipy.ndimage import affine_transform
import cv2
from glob import glob


def calculate_affine(srcPoints, dstPoints):
    # Add a fourth coordinate of 1 to each point
    srcPoints = np.hstack((srcPoints, np.ones((srcPoints.shape[0], 1))))
    dstPoints = np.hstack((dstPoints, np.ones((dstPoints.shape[0], 1))))
    # Solve the system of linear equations
    affine_matrix, _, _, _ = np.linalg.lstsq(srcPoints, dstPoints, rcond=None)
    return affine_matrix.T


def read_ants_affine(aff_path):
    ants_affine = ants.read_transform(aff_path)
    before_points = np.array([[0, 0], [0, 1], [1, 0]])
    after_points = np.array([ants_affine.apply_to_point(p) for p in before_points])
    # calculate the affine matrix
    affine_matrix = calculate_affine(before_points, after_points)
    return affine_matrix


def apply_affine_to_points(affine_matrix, points):
    # Convert the points to homogeneous coordinates
    points_homogeneous = np.column_stack((points, np.ones(points.shape[0])))
    # Apply the transformation
    points_transformed_homogeneous = np.dot(affine_matrix, points_homogeneous.T).T
    # Convert the transformed points back to 2D
    points_transformed_2d = points_transformed_homogeneous[:, :2]
    return points_transformed_2d


def read_nonlinear(non_linear_path):
    non_linear = nib.load(non_linear_path)
    non_linear_data = non_linear.get_fdata()
    # remove dimensions of size 1
    non_linear_data = np.squeeze(non_linear_data)
    height = non_linear_data.shape[0]
    width = non_linear_data.shape[1]
    return non_linear_data, height, width


def apply_nonlinear_to_image(moving_image, non_linear_data, mode="nearest"):
    non_linear_reorder = np.moveaxis(non_linear_data, [0, 1, 2], [1, 2, 0])
    grid = np.mgrid[0 : moving_image.shape[0], 0 : moving_image.shape[1]]
    warp_grid = non_linear_reorder + grid
    warped_image = scipy.ndimage.map_coordinates(
        moving_image, warp_grid, order=0, mode=mode
    )
    return warped_image


def apply_affine_to_image(moving_image, affine_matrix, output_shape, mode="constant"):
    # convert image to grayscale
    if len(moving_image.shape) == 3:
        moving_image = rgb2gray(moving_image)
    output_height, output_width = output_shape
    pad_top_bottom = output_height - moving_image.shape[0]
    pad_left_right = output_width - moving_image.shape[1]
    pad_top = pad_top_bottom // 2
    pad_bottom = pad_top_bottom - pad_top
    pad_left = pad_left_right // 2
    pad_right = pad_left_right - pad_left
    if pad_top < 0:
        moving_image = moving_image[-pad_top:, :]
        pad_top = 0
    if pad_bottom < 0:
        moving_image = moving_image[:pad_bottom, :]
        pad_bottom = 0
    if pad_left < 0:
        moving_image = moving_image[:, -pad_left:]
        pad_left = 0
    if pad_right < 0:
        moving_image = moving_image[:, :pad_right]
        pad_right = 0

    moving_image = np.pad(
        moving_image, ((pad_top, pad_bottom), (pad_left, pad_right)), mode=mode
    )
    affine_matrix[2, :] = [0, 0, 1]
    adjusted_image = affine_transform(moving_image, affine_matrix, order=0)
    return adjusted_image
