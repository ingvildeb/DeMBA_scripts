from utils.QuickNII_functions import read_QUINT_JSON, find_plane_equation 
from utils.generate_target_slice import generate_target_slice
import numpy as np
import cv2
import matplotlib.pyplot as plt
import nrrd
import sympy as sp

from sympy import symbols, solve





def generate_rectangular_image(img, pts):

    # Define the four pixel coordinates of the output image (i.e., the corners of the new rectangular image)
    width = max(np.sqrt(((pts[0][0]-pts[1][0])**2)+((pts[0][1]-pts[1][1])**2)), np.sqrt(((pts[2][0]-pts[3][0])**2)+((pts[2][1]-pts[3][1])**2)))
    height = max(np.sqrt(((pts[0][0]-pts[3][0])**2)+((pts[0][1]-pts[3][1])**2)), np.sqrt(((pts[1][0]-pts[2][0])**2)+((pts[1][1]-pts[2][1])**2)))
    output_pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    pts = pts.astype(np.float32)
    
    # Compute the perspective transformation matrix using cv2.getPerspectiveTransform() function
    M = cv2.getPerspectiveTransform(pts, output_pts)

    # Apply the perspective transformation using cv2.warpPerspective() function
    output_img = cv2.warpPerspective(img, M, (int(width), int(height)))

    return output_img

def generate_padded_image(img, pts):
    # Define the four pixel coordinates of the input image
    pts = np.array(pts)
    imheight, imwidth = img.shape


    left_pad = np.abs(np.min((0,np.min(pts[:,0])) ))
    right_pad = np.max((0,np.max(pts[:,0]) - (imwidth - left_pad)))

    top_pad = np.abs(np.min((0,np.min(pts[:,1])) ))
    bottom_pad =  np.max((0,np.max(pts[:,1]) - (imheight - top_pad)))

    img = cv2.copyMakeBorder(img, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=[0, 0, 0])



    adjusted_pts = pts.copy()


    adjusted_pts[:,0] += left_pad


    adjusted_pts[:,1] += top_pad
   




    return img,adjusted_pts


def find_combination(alignment, target):
    # Define the three vectors
    v1 = alignment[:3]
    v2 = alignment[3:6]
    v3 = alignment[6:]
    x4, y4, z4 = target
    # Define the target vector
    target = np.array([x4, y4, z4])

    # Define the matrix A and vector b for the least squares method
    A = np.vstack([v2, v3]).T
    b = target - v1

    # Compute the values of M and N using the least squares method
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    M, N = x

    # Compute the result vector closest to the target vector
    result = v1 + M*v2 + N*v3
    # print(f"Target vector: {target}")
    # print(f"Result vector: {result}")
    return M, N


def find_vector(data, dest = 'Zero'):
    x = symbols('x')
    if dest=='Zero':
        target_ratio = data[0] / data[2]
        expr = (np.mean((data[3:6]*x,data[6:]), axis=-0)[0] / np.mean((data[3:6]*x,data[6:]), axis=-0)[2]) - target_ratio
        solution = solve(expr)
        vector =  np.mean((data[3:6]*solution,data[6:]), axis=-0)
        magnitude =  (data[0],  data[2]) / vector[[0,2]]
        magnitude =  np.mean((magnitude[0], magnitude[1]))

    if dest=='X':
        expr = (np.mean((data[3:6].values*x,data[6:]), axis=-0)[2] / np.mean((data[6:]*x,data[3:6]), axis=-0)[2]) 
        solution = solve(expr)
        vector =  np.mean((data[3:6]*solution,data[6:]), axis=-0)
        magnitude =  1/ vector[0]

    if dest=='Z':
        expr = (np.mean((data[3:6].values*x,data[6:]), axis=-0)[0] / np.mean((data[3:6]*x,data[6:]), axis=-0)[2]) 
        solution = solve(expr)
        vector =  np.mean((data[3:6].values*solution,data[6:]), axis=-0)
        magnitude =  1/ vector[2]
    
    return solution, vector, magnitude

def perfect_image(img, alignment, resolution=25):

    x_size = 11400 / resolution
    y_size = 8000 / resolution
    
    (cx, cy, cz), k = find_plane_equation(alignment)

    top_leftX, top_leftZ = 0,0
    top_leftY = -(cx*top_leftX + cy + top_leftZ*cz + k) / cy
    top_left = (top_leftX, top_leftY, top_leftZ)


    top_rightX, top_rightZ = x_size, 0
    top_rightY = -(cx*top_rightX + cy + top_rightZ*cz + k) / cy
    top_right = (top_rightX, top_rightY, top_rightZ)

    bottom_rightX, bottom_rightZ = x_size,y_size
    bottom_rightY = -(cx*bottom_rightX + cy + bottom_rightZ*cz + k) / cy
    bottom_right = (bottom_rightX, bottom_rightY, bottom_rightZ)

    bottom_leftX, bottom_leftZ = 0,y_size
    bottom_leftY = -(cx* bottom_leftX + cy + bottom_leftZ*cz + k) / cy
    bottom_left = (bottom_leftX, bottom_leftY, bottom_leftZ)

    size = np.array((np.linalg.norm(alignment[3:6]), np.linalg.norm(alignment[6:9]))).round().astype(int)
    img = cv2.resize(img, size)
    imheight, imwidth = img.shape

    tlM, tlN = find_combination(alignment, top_left)
    tlX = np.round(tlM * imwidth).astype(int)
    tlY = np.round(tlN * imheight).astype(int)

    trM, trN = find_combination(alignment, top_right)
    trX = np.round(trM * imwidth).astype(int)
    trY = np.round(trN * imheight).astype(int)

    brM, brN = find_combination(alignment, bottom_right)
    brX = np.round(brM * imwidth).astype(int)
    brY = np.round(brN * imheight).astype(int)

    blM, blN = find_combination(alignment, bottom_left)
    blX = np.round(blM * imwidth).astype(int)
    blY = np.round(blN * imheight).astype(int)
    # Define the four pixel coordinates of the input image
    pts = np.array([(tlX, tlY), (trX, trY), (brX, brY), (blX, blY)])
    # Pad the input image with zeros to handle out of bounds pixel coordinates
    pad_img, pts = generate_padded_image(img, pts)
    # Generate the new rectangular image with the given four pixel coordinates as the corners
    output_img = generate_rectangular_image(pad_img, pts)
    return output_img, pts

