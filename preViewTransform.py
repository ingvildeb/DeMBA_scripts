%matplotlib qt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from tkinter import filedialog
import SimpleITK as sitk
import nibabel as nib
import numpy as np

# define the fixed and moving image

age = "P28"


working_path = "C:/Users/ingvieb/Elastix_testing/P28/"

#Target volume
DeMBAVolumePath = working_path + age + "_DeMBA_template.nii.gz"

#Fixed volume (OLD)
CCFVolumePath = working_path + "result_segmentation-test3.nii"
CCFVolumePath = filedialog.askopenfilename(title="OLD Volume")

#Moved Volume (NEW)
MovedVolumePath = working_path + "result_segmentation-test-nolms.nii"
MovedVolumePath = filedialog.askopenfilename(title="New Volume")

##Load the volumes using nib and convert them to numpy arrays
DeMBAVolume = nib.load(DeMBAVolumePath)
DeMBAVolume = np.array(DeMBAVolume.dataobj)

CCFVolume = nib.load(CCFVolumePath)
CCFVolume = np.array(CCFVolume.dataobj)


MovedVolume = nib.load(MovedVolumePath)
MovedVolume = np.array(MovedVolume.dataobj)


# Define two 3D volumes as numpy arrays
volume1 = DeMBAVolume


volume2 = MovedVolume


#Before Image
volume3 = CCFVolume


# Define the maximum and minimum slice numbers
max_slice = volume1.shape[2]-1
min_slice = 0
# Define the initial slice numbers
slice1 = 200
slice2 = 200








import matplotlib as mpl
import matplotlib.cm as cm
   
norm = mpl.colors.Normalize(vmin=0, vmax=1)
cmap = cm.plasma

m = cm.ScalarMappable(norm=norm, cmap=cmap)
cmapGray = cm.gray

gray = cm.ScalarMappable(norm=norm, cmap=cmapGray)





#atlas ids dont plot well, make them nicer
def view_atlas_image(image, flip=False):
    if flip:
        image = image[::-1, ::-1]
    regions = np.unique(image)
    regions_replace = np.arange(0, len(regions))
    viewable_slice = np.zeros(image.shape)
    for region, region_rep in zip(regions, regions_replace):
        mask = image == region
        viewable_slice[mask] = region_rep
    return viewable_slice




# Define a function to update the plot when the slider value changes
def update_slices(val):
    slice1 = int(slider1.val)
    slice2 = int(slider1.val)
    
    opacity = float(slider2.val)
    im1 = volume1[:, :, slice1] 
    
    
    atlas = view_atlas_image(volume2[:, :, slice2]) 

    atlas = (atlas + abs(np.min(atlas))) /np.max(atlas)
    
    
        
    OldAtlas = view_atlas_image(volume3[:, :, slice2]) 

    OldAtlas = (OldAtlas + abs(np.min(OldAtlas))) /np.max(OldAtlas)
    
    
    
    im1 = (im1 + abs(np.min(im1)) )/np.max(im1)

    average_im = gray.to_rgba(im1) + ( m.to_rgba(atlas) * opacity)
    #OldAtlas = OldAtlas
    #stack_old = np.stack([im1, OldAtlas], axis=2)

   # average_im_old = np.average(stack_old, axis=2 )
    average_im_old = gray.to_rgba(im1) + ( m.to_rgba(OldAtlas) *   opacity)
    # Update the slice images in the existing subplots
    axs[0].images[0].set_array(average_im_old)
    axs[0].set_title('Old, slice {}'.format(slice1))
    axs[1].images[0].set_array(average_im)
    axs[1].set_title('New, slice {}'.format(slice2))
    # Redraw the plot
    fig.canvas.draw_idle()
    
    
    
    
    
    
    
# Create the figure and subplots
fig, axs = plt.subplots(1, 2, sharex=True, sharey=True)
# Show the slices of the first volume
im1 = volume1[:, :, slice1]

atlas = view_atlas_image(volume2[:, :, slice2]) 

atlas = atlas/np.max(atlas)
im1 = im1 /np.max(im1)


average_im = gray.to_rgba(im1) + m.to_rgba(atlas)

    
OldAtlas = view_atlas_image(volume3[:, :, slice2]) 

OldAtlas = (OldAtlas + abs(np.min(OldAtlas))) /np.max(OldAtlas)


average_im_old = gray.to_rgba(im1) + m.to_rgba(OldAtlas)

print(average_im_old.shape)


axs[0].imshow(average_im_old, cmap=None)
axs[0].set_title('Old , slice {}'.format(slice1))
# Show the slices of the second volume
axs[1].imshow(average_im, cmap=None)
axs[1].set_title('New , slice {}'.format(slice2))
# Add the slider widgets
slider1_ax = plt.axes([0.1, 0.05, 0.8, 0.02])
slider1 = Slider(slider1_ax, 'Volume 1', min_slice, max_slice, valinit=slice1, valstep=1)
slider2_ax = plt.axes([0.1, 0.01, 0.8, 0.02])
slider2 = Slider(slider2_ax, 'Atlas opacity', 0, 1, valinit=0.5, valstep=0.05)

# Attach the update_slices function to the slider widgets
slider1.on_changed(update_slices)
slider2.on_changed(update_slices)

# Show the plot
plt.show()




