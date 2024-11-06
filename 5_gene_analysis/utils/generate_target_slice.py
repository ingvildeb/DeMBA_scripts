import numpy as np
import math


def calculate_XYZ_pad_old(alignment, bounds):
    """
    alignment is a quicknii alignment
    bounds is the shape of the volume minus 1
    """
    Ox, Oy, Oz, Ux, Uy, Uz, Vx, Vy, Vz = alignment
    #bounds = np.array(volume.shape) - 1
    X_size = np.sqrt(np.sum(np.square((Ux, Uy, Uz))))
    Z_size = np.sqrt(np.sum(np.square((Vx, Vy, Vz))))
    X_size = np.round(X_size).astype(int)
    Z_size = np.round(Z_size).astype(int)
    Uarange = np.arange(0, 1, 1 / X_size)
    Varange = np.arange(0, 1, 1 / Z_size)
    Ugrid, Vgrid = np.meshgrid(Uarange, Varange)
    Ugrid_x = Ugrid * Ux
    Ugrid_y = Ugrid * Uy
    Ugrid_z = Ugrid * Uz
    Vgrid_x = Vgrid * Vx
    Vgrid_y = Vgrid * Vy
    Vgrid_z = Vgrid * Vz

    X_Coords = (Ugrid_x + Vgrid_x).flatten() + Ox
    Y_Coords = (Ugrid_y + Vgrid_y).flatten() + Oy
    Z_Coords = (Ugrid_z + Vgrid_z).flatten() + Oz

    X_Coords = np.round(X_Coords).astype(int)
    Y_Coords = np.round(Y_Coords).astype(int)
    Z_Coords = np.round(Z_Coords).astype(int)

    out_bounds_Coords = (
        (X_Coords > bounds[0]) | (Y_Coords > bounds[1]) | (Z_Coords > bounds[2]) 
        | (X_Coords < 0) | (Y_Coords < 0) | (Z_Coords < 0)
    )

    X_pad = X_Coords.copy()
    Y_pad = Y_Coords.copy()
    Z_pad = Z_Coords.copy()

    X_pad[out_bounds_Coords] = 0
    Y_pad[out_bounds_Coords] = 0
    Z_pad[out_bounds_Coords] = 0

    return X_pad, Y_pad, Z_pad

def generate_target_coordinates(ouv, atlas_shape):
    width = None
    height = None
    ox, oy, oz, ux, uy, uz, vx, vy, vz = ouv
    width = np.floor(math.hypot(ux,uy,uz)).astype(int) + 1
    height = np.floor(math.hypot(vx,vy,vz)).astype(int) + 1
    data = np.zeros((width, height), dtype=np.uint32).flatten()
    xdim, ydim, zdim = atlas_shape
    y_values = np.arange(height)
    x_values = np.arange(width)
    hx = ox + vx * (y_values / height)
    hy = oy + vy * (y_values / height)
    hz = oz + vz * (y_values / height)
    wx = ux * (x_values / width)
    wy = uy * (x_values / width)
    wz = uz * (x_values / width)
    lx = np.floor(hx[:, None] + wx).astype(int) 
    ly = np.floor(hy[:, None] + wy).astype(int) 
    lz = np.floor(hz[:, None] + wz).astype(int) 
    valid_indices = (0 <= lx) & (lx < xdim) & (0 <= ly) & (ly < ydim) & (0 <= lz) & (lz < zdim)
    valid_indices_flat = valid_indices.flatten()
    lxf = lx.flatten()
    lyf = ly.flatten()
    lzf = lz.flatten()
    valid_lx = lxf[valid_indices_flat]
    valid_ly = lyf[valid_indices_flat]
    valid_lz = lzf[valid_indices_flat]
    return valid_lx, valid_ly, valid_lz, height, width, valid_indices

def calculate_regions(X_pad, Y_pad, Z_pad, volume, X_size, Z_size):
    regions = volume[X_pad, Y_pad, Z_pad]

    C = len(regions)
    compare = C - X_size * Z_size
    if abs(compare) == X_size:
        if compare > 0:
            Z_size += 1
        if compare < 0:
            Z_size -= 1
    elif abs(C - X_size * Z_size) == Z_size:
        if compare > 0:
            X_size += 1
        if compare < 0:
            X_size -= 1
    elif abs(C - X_size * Z_size) == Z_size + X_size + 1:
        if compare > 0:
            X_size += 1
            Z_size += 1
        if compare < 0:
            X_size -= 1
            Z_size -= 1
    elif abs(C - X_size * Z_size) == abs(Z_size - X_size):
        if compare > 0:
            X_size += 1
            Z_size -= 1
        if compare < 0:
            X_size -= 1
            Z_size += 1

    regions = regions.reshape((abs(Z_size), abs(X_size)))
    return regions


def generate_target_slice(ouv, atlas):
    width = None
    height = None
    ox, oy, oz, ux, uy, uz, vx, vy, vz = ouv
    width = np.floor(math.hypot(ux,uy,uz)).astype(int) + 1
    height = np.floor(math.hypot(vx,vy,vz)).astype(int) + 1
    data = np.zeros((width, height), dtype=np.uint32).flatten()
    xdim, ydim, zdim = atlas.shape
    y_values = np.arange(height)
    x_values = np.arange(width)
    hx = ox + vx * (y_values / height)
    hy = oy + vy * (y_values / height)
    hz = oz + vz * (y_values / height)
    wx = ux * (x_values / width)
    wy = uy * (x_values / width)
    wz = uz * (x_values / width)
    lx = np.floor(hx[:, None] + wx).astype(int) 
    ly = np.floor(hy[:, None] + wy).astype(int) 
    lz = np.floor(hz[:, None] + wz).astype(int) 
    valid_indices = (0 <= lx) & (lx < xdim) & (0 <= ly) & (ly < ydim) & (0 <= lz) & (lz < zdim)
    valid_indices = valid_indices.flatten()
    lxf = lx.flatten()
    lyf = ly.flatten()
    lzf = lz.flatten()
    valid_lx = lxf[valid_indices]
    valid_ly = lyf[valid_indices]
    valid_lz = lzf[valid_indices]
    atlas_slice = atlas[valid_lx,valid_ly,valid_lz]
    data[valid_indices] = atlas_slice
    data_im = data.reshape((height, width))
    return data_im