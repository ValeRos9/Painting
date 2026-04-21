#libraries
from __future__ import division
import numpy as np 
import random
import sys
from .Painting import Painting

class Painting_generator:
    def __init__(self,dim_x,dim_y,thickness,layers_val,N_spheres,radius,sphere_val):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.thickness = thickness
        self.layers_val = layers_val
        self.N_spheres = N_spheres 
        self.radius = radius
        self.sphere_val = sphere_val
        print(layers_val)
    
    def paint(self):
        """creates a Painting, generating volume, inserting spheres and adding intensity values"""

        Sheet = np.empty((np.sum(self.thickness),self.dim_y,self.dim_x,))
        for idx_layer in range(self.thickness.size):

            #Set intensity value for Paint Layer and generate spheres (the view is from the front of the Painting)
            if idx_layer == 0: 
                start_idx = idx_layer
                end_idx = self.thickness[idx_layer]

                Sheet[start_idx:end_idx,:,:] = self.layers_val[idx_layer]

                if self.thickness[idx_layer] < 2 * self.radius + 1:
                    print("Error! thickness of Paint layer", self.thickness[idx_layer], "is too small compared with r_sphere=", self.radius,",radius can't be more than",(self.thickness[idx_layer]-1)/2)
                    raise SystemExit(1)
                else:
                    centers = self.random_insert_spheres(Sheet[start_idx:end_idx,:,:], self.N_spheres, self.radius, self.sphere_val)

            #Set intensity values for subsequent Layers (Ground/Wodd Layer)
            else: 
                start_idx = np.sum(self.thickness[0:idx_layer])
                end_idx = np.sum(self.thickness[0:idx_layer+1]) #+1 is needed to iterate through the full array

                Sheet[start_idx:end_idx,:,:]=self.layers_val[idx_layer]
        
        return Painting(Sheet)

    @staticmethod
    def random_insert_spheres(layer, nspheres, r, intensity):
        """Generates valid center points and insert a sphere of radius r at those points"""

        #Creates a box with at center a standard sphere of radius r
        x,y,z = np.meshgrid(np.arange(2*r+1), np.arange(2*r+1), np.arange(2*r+1), indexing='ij')
        mask = (x - r)**2 + (y - r)**2 + (z - r)**2  <= r**2

        centers = []
        attempts = 0
        while len(centers) < nspheres and attempts < 1000:  

            #Generates potential center points, using boundary conditions r<=x,y,z<n-r
            c0 = round(r+random.random()*(layer.shape[0]-1-2*r))
            c1 = round(r+random.random()*(layer.shape[1]-1-2*r))
            c2 = round(r+random.random()*(layer.shape[2]-1-2*r))
            collision = False

            #Check if potential center points overlap with other spheres
            for c in centers:
                if (c0-c[0])**2+(c1-c[1])**2+(c2-c[2])**2 <= 4*r*r:
                    collision=True
                    attempts += 1
                    break

            if not collision:
                centers.append((c0,c1,c2))
                layer[c0-r:c0+r+1,c1-r:c1+r+1,c2-r:c2+r+1][mask] = intensity
                attempts = 0
                
        print("N_centers",len(centers))
        return centers


"""
remarks: 
1.If you have multiple paint/ground layers, you could add a list as input to the method to choose multiple
2. Example of potential optimization
@staticmethod
def generate_centers(layer, nspheres, r, intensity):
    shape = np.array(layer.shape[:3])
    if np.any(shape <= 2*r): return []
    
    # Precompute sphere mask
    d = 2*r + 1
    x, y, z = np.meshgrid(np.arange(d), np.arange(d), np.arange(d), indexing='ij')
    mask = (x-r)**2 + (y-r)**2 + (z-r)**2 <= r**2
    
    centers = []
    attempts = 0

    while len(centers) < nspheres and attempts < nspheres * 2000:
        # Generate batch of candidates
        batch = np.random.randint(r, shape - 2*r, size=(min(500, nspheres-len(centers)), 3))
        
        if centers:
            c_arr = np.array(centers)
            # Vectorized distance check: (batch, 1, 3) - (1, n, 3)
            dists = np.sum((batch[:, None, :] - c_arr[None, :, :])**2, axis=2)
            valid = batch[~np.any(dists <= 4*r*r, axis=1)]
        else:
            valid = batch
            
        for c in valid:
            if len(centers) >= nspheres: break
            centers.append(tuple(c))
            layer[c[0]-r:c[0]+r+1, c[1]-r:c[1]+r+1, c[2]-r:c[2]+r+1][mask] = intensity
        attempts += len(batch)
        
    return centers
"""