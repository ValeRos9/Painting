import numpy as np
from scipy.optimize import least_squares
from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography

def check_slices(layer,xc,yc,zc,r,intensity):
    # Extract slices through the center
    slice_x = layer[xc, :, :] 
    slice_y = layer[:, yc, :] 
    slice_z = layer[:, :, zc] 

    slices = [slice_x, slice_y, slice_z]
    centers_2d = [(yc, zc), (xc, zc), (xc, yc)]
    
    tolerance = 1.2  #tolerance paramter, allows for "staircase" effect 
    
    for i, (slice_2d, center) in enumerate(zip(slices, centers_2d)): 
        c1, c2 = center
        coords = np.argwhere(slice_2d == intensity)
        dists = np.sqrt((coords[:, 0] - c1)**2 + (coords[:, 1] - c2)**2)
        
        if len(coords) == 0:
            print(f"FAIL: Slice {i} is empty.")
            return False
            
        # CHECK 1: Does it extend too far? (Catches cubes, ellipsoids)
        if np.max(dists) > r + tolerance:
            print(f"FAIL: Slice {i} extends to {np.max(dists):.2f}, expected max ~{r + tolerance}")
            return False
            
        # CHECK 2: Does it fill out enough? (Catches diamonds, stars, under-filled)
        # A circle should fill out to at least r - tolerance in most directions.
        # We check if the 90th percentile of distances is close to r.
        p90_dist = np.percentile(dists, 90)
        if p90_dist < r - tolerance:
            print(f"FAIL: Slice {i} is too small (90% of pixels within {p90_dist:.2f}).")
            return False
        
        # 3. Check Inner Fill (Catch hollow spheres, rings, stars)
        # The closest pixel should be near the center (0), unless it's a hollow shell.
        # For a SOLID sphere, min_dist should be 0 (the center pixel itself).
        # If you are testing a HOLLOW shell, change this check to: abs(min_dist - r) < tolerance
        if np.min(dists) > 1.0: 
            print(f"FAIL: Slice {i} has a hole in the center (Min dist: {min_dist:.2f})")
            return False
            
    return True

"""
def check_spheres(layer,center):
    layer[all pixels below and above xc by r must be 0]
    layer[all pixels below and above yc by r must be 0]
    layer[all pixels below and above zc by r must be 0]
"""

#initialize
dim_x=10
dim_y=10
thickness= np.array([10])
intensity_layer = np.array([0])
intensity_sphere = 1 
N_spheres= 1
r= 2


#Create layer 
artist = Painting_generator(dim_x,dim_y,thickness,intensity_layer,N_spheres,r)
Painting = artist.paint()
center = artist.select_random_indices(Painting.volume,1)
print(center)




