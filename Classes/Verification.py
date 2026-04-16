import numpy as np
from scipy import ndimage


class Verification:
    def __init__(self,xc,yc,zc,radius):
        self.xc = xc
        self.yc = yc
        self.yc = zc
        self.radius = radius
        self.intensity = N_spheres 
        self.radius = radius
    
    def check_slices(self):

        """"
        Extract the 3 orthogonal slices of a discretized circle and checks
        if the desired shape is a discretized circle, using a tolerance parameter
        """

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
                print(f"FAIL: Slice {i} extends to {max_dist:.2f}, expected max ~{r + tolerance}")
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
    Sphere coords (c,r) extraction, might be useful for later
    def extract_sphere_parameters(3d_array,intensity):
        "Extracts center and radius of a discretized sphere from a 3D array"

        #Extract position of values with sphere 
        coords = np.argwhere(layer == intensity)

        #Perform a test
        if len(coords) == 0:
            raise ValueError("No filled voxels found in the array.")
        
        #Compute center and radius for discretized sphere 
        center = coords.mean(axis=0)
        radius_perfect_circle = np.sqrt(np.sum((coords - center)**2, axis=1))
        radius = np.percentile(radius_perfect_circle, 96)

        return center, radius 

    def extract_sphere_parameters(3d_array, intensity):
        "
        Extracts centers and radii for multiple disjoint spheres in a 3D array.
        "
        #Separate spheres into multiple departements 
        mask = (layer == intensity)
        labeled_array, num_features = ndimage.label(mask, structure=np.ones((3, 3, 3)))
        
        if num_features == 0:
            return []

        results = []

        # 2. Iterate over each detected sphere
        for i in range(1, num_features + 1):
            # Extract coordinates for the current label only
            coords = np.argwhere(labeled_array == i)

            if len(coords) == 0:
                continue

            # Calculate Center (Centroid)
            center = coords.mean(axis=0)
            perfect_radius = np.sqrt(np.sum((coords - center)**2, axis=1))
            radius = np.percentile(perfect_radius, 96)
            
            results.append({
                'label': i,
                'center': center,
                'radius': radius,
                'voxel_count': len(coords)
            })

        return results
    """