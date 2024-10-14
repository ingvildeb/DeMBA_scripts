from glob import glob
import json
import CCF_translator
import cv2
from utils.generate_target_slice import generate_target_slice, generate_target_coordinates
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from utils.deform_utils import triangulate, transform_vec
import nibabel as nib
from utils.NearestNDInterpolator import NearestNDInterpolator
from brainglobe_atlasapi.bg_atlas import BrainGlobeAtlas
from scipy.ndimage import zoom

def non_linear(image, h,w,m):
    m = np.array(m)
    im_h, im_w = image.shape
    if (im_h, im_w)!=(h,w):
        h_scale = im_h / h
        w_scale = im_w / w
        m[:,[0,2]] *= w_scale
        m[:,[1,3]] *= h_scale
        h,w = im_h, im_w    
    y,x = np.mgrid[:h, :w]
    triangulation = triangulate(w,h,m)
    nx,ny = transform_vec(triangulation, x.flatten(),y.flatten())
    nx = nx.reshape(x.shape)
    ny = ny.reshape(y.shape)
    nx = np.round(nx).astype(int)
    ny = np.round(ny).astype(int)
    out_image = np.zeros(image.shape)
    valid = (ny>0) & (ny < h) & (nx>0) & (nx < w)
    out_image[ny[valid],nx[valid]] = image[y[valid],x[valid]]
    return out_image

key_ages = [56, 28, 14, 4]
seg_images = glob("/home/harryc/github/AllenDownload/downloaded_data/*/*/expression/*.jpg")
for age in tqdm(key_ages[:]):
    path = r"/mnt/z/HBP_Atlasing/Developmental_atlases/DeMBA_Developmental mouse brain atlas/DeMBA-v1/01_working-environment/01_Data/Allen_Dev_ISH/nutil-v2"
    alignment_path = f"{path}/P{age}/images/onlyCalbJSON.json"
    with open(alignment_path) as r:
        alignment = json.load(r)

    atlas_shape = np.array(alignment['target-resolution']).astype(int)
    fill_volume =  np.zeros(atlas_shape) 
    valid_vol = np.zeros(atlas_shape) 
    for a in tqdm(alignment['slices'][:]):
        seg_path = [i for i in seg_images if a['filename'].replace('png', 'jpg').replace('_s', '_s0') in i][0]
        segmentation = cv2.imread(seg_path)[:,:,0]
        ouv = a['anchoring']
        tx,ty,tz,h,w,valid_ind = generate_target_coordinates(ouv, atlas_shape)
        seg_small = cv2.resize(segmentation, (w,h),interpolation=cv2.INTER_AREA)
        if "markers" in a:
            non_lin_seg_small = non_linear(seg_small, a['height'], a['width'], a['markers'])
        else:
            non_lin_seg_small = seg_small
        fill_volume[tx,ty,tz] = non_lin_seg_small[valid_ind]
        valid_vol[tx, ty, tz] = 1
        

    valid_vol = valid_vol.astype(bool)
    ##Interpolation


    atlas = BrainGlobeAtlas('allen_mouse_10um')
    atlas_volume = atlas.annotation
    atlas_volume = zoom(atlas_volume, 0.5, order=0)

    # atlas_volume = np.transpose(atlas_volume,[2,0,1])[:,::-1,::-1]
    # atlas_volume = np.pad(atlas_volume, ((0,0),(45,0),(0,0)))

    ccfAtlas = CCF_translator.Volume(atlas_volume, age_PND = 56, segmentation_file=True, space='allen_mouse',voxel_size_micron=20)
    ccfAtlas.transform(target_space='demba_dev_mouse', target_age=age)
    ccfAtlas.values = ccfAtlas.values.transpose([0,2,1])
    ccfAtlas.values = ccfAtlas.values[:,::-1,::-1]



    output_volume = fill_volume.copy()

    brain_mask = ccfAtlas.values != 0
    indices_to_fit = brain_mask & valid_vol
    indices_to_fill = brain_mask & ~valid_vol
    k = 100
    grid = np.mgrid[0 : atlas_shape[0], 0 : atlas_shape[1], 0 : atlas_shape[2]]
    points = grid.reshape((3, -1)).T
    interpolator = NearestNDInterpolator(points[indices_to_fit.flatten()], fill_volume[indices_to_fit])
    output_volume[indices_to_fill] = interpolator(points[indices_to_fill.flatten()], k=k)
    #we can now perform the interpolation on the values on the section
    #This is done so as to make the volume appear homogenous and remove streaking.
    interpolator = NearestNDInterpolator(points[indices_to_fill.flatten()], output_volume[indices_to_fill])
    output_volume[indices_to_fit] = interpolator(points[indices_to_fit.flatten()], k=k)

    aff = np.eye(4)
    aff[:3,:3] *= 0.02
    out = nib.Nifti1Image(output_volume, aff)
    nib.save(out, f'new_P{age}_gene_vol_all.nii.gz')




