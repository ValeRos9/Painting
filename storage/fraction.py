import numpy as np

def insert_sphere(layer, center, r, intensity):
    frac = sphere_fraction_fast(r, center)

    cx, cy, cz = center
    n = frac.shape[0]

    x0 = int(np.floor(cx)) - r
    y0 = int(np.floor(cy)) - r
    z0 = int(np.floor(cz)) - r

    layer[x0:x0+n,y0:y0+n,z0:z0+n] += intensity * frac

def personalized_round(val):
    if val <= 0.5:
        return 
    else
        return 

def sphere_fraction_fast(r, center):




    cx, cy, cz = center
    c0= cx-round(cx)
    c1= cy-round(cy)
    c2= cz-round(cz)
    print(c0,c1,c2)
    n = 2 * r + 1

    x = np.arange(n) - r
    y = np.arange(n) - r
    z = np.arange(n) - r


    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    print(X,Y,Z)

    # distance from voxel centers to sphere center
    d = np.sqrt((X - c0)**2 + (Y - c1)**2 + (Z - c2)**2)


    # voxel half-diagonal (controls transition thickness)
    h = np.sqrt(3) / 2

    frac = np.zeros_like(d, dtype=np.float32)

    # fully inside
    frac[d <= r - h] = 1.0

    # fully outside
    frac[d >= r + h] = 0.0

    # boundary region (smooth interpolation)
    mask = (d > r - h) & (d < r + h)

    t = (r + h - d[mask]) / (2 * h)
    frac[mask] = t * t * (3 - 2 * t)  # smoothstep
    print(frac)
    return frac

sphere_fraction_fast(r=1,center=(3.5,4.6,5.2))
