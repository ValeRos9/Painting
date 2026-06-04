import numpy as np


def sphere_fraction_voxel(r):
    n = 2*r + 1

    #Voxel centered grid 
    X, Y= np.meshgrid(np.arange(n) - r, np.arange(n) - r, indexing='ij')

    d = np.sqrt(X**2 + Y**2)

    # voxel half-diagonal (worst-case distance inside voxel)
    h = np.sqrt(2) / 2

    frac = np.zeros_like(d, dtype=np.float32)

    # fully inside sphere
    frac[d <= r - h] = 1.0

    # fully outside sphere
    frac[d >= r + h] = 0.0

    # partial voxels (smooth interpolation band)
    mask = (d > r - h) & (d < r + h)

    t = (r + h - d[mask]) / (2*h)
    frac[mask] = t*t*(3 - 2*t)

    return frac



def MC_vectorized(r)
    n = 2*r + 1
    oversample = 50

    u = (np.arange(oversample) + 0.5) / oversample - 0.5
    dx, dy, dz = np.meshgrid(u, u, u, indexing='ij')

    dx = dx.reshape(-1)
    dy = dy.reshape(-1)
    dz = dz.reshape(-1)

    N = dx.size

    # voxel centers grid
    i = np.arange(n) - r
    j = np.arange(n) - r
    k = np.arange(n) - r

    I, J, K = np.meshgrid(i, j, k, indexing='ij')

    frac = np.zeros((n, n, n), dtype=np.float32)

    for s in range(N):
        x = I + dx[s]
        y = J + dy[s]
        z = K + dz[s]

        frac += (x*x + y*y + z*z <= r*r)

    frac /= N
return frac


def sphere_fraction_method_B(r, oversample=6):
    n = 2*r + 1

    # --- voxel grid (centers) ---
    x = np.arange(n) - r
    y = np.arange(n) - r
    z = np.arange(n) - r

    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    d = np.sqrt(X**2 + Y**2 + Z**2)

    # voxel half-diagonal
    h = np.sqrt(3) / 2

    frac = np.zeros((n, n, n), dtype=np.float32)

    # --- classify regions ---
    inside_mask   = d <= (r - h)
    outside_mask  = d >= (r + h)
    boundary_mask = ~(inside_mask | outside_mask)

    # --- exact regions ---
    frac[inside_mask] = 1.0
    frac[outside_mask] = 0.0

    # --- MC only on boundary voxels ---
    if np.any(boundary_mask):

        # precompute subvoxel offsets once
        u = (np.arange(oversample) + 0.5) / oversample - 0.5
        dx, dy, dz = np.meshgrid(u, u, u, indexing='ij')

        dx = dx.ravel()
        dy = dy.ravel()
        dz = dz.ravel()
        N = dx.size

        # boundary voxel coordinates
        vox = np.argwhere(boundary_mask)

        # vectorized MC
        cx = vox[:, 0][:, None] - r
        cy = vox[:, 1][:, None] - r
        cz = vox[:, 2][:, None] - r

        x = cx + dx
        y = cy + dy
        z = cz + dz

        inside = (x*x + y*y + z*z <= r*r)

        frac_boundary = inside.mean(axis=1)

        # write back
        frac[boundary_mask] = frac_boundary

    return frac

r = 1

print(sphere_fraction_voxel(r))