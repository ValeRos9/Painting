#libraries
from __future__ import division
import numpy as np 
import random
import sys
from .Painting import Painting
from .mu import Attenuation

class Painting_generator:
    def __init__(self,E,layer_type,pigment,height,width,thickness,N_spheres,radius): 
        self.E = E
        self.layer_type = layer_type
        self.pigment = pigment
        self.height = height
        self.width = width
        self.thickness = thickness 
        self.N_spheres = N_spheres 
        self.radius = radius

    def paint(self):
        """generates a volume, inserts spheres and adds mu values"""

        #Generate Painting volume
        volume = np.empty((sum(self.thickness),self.width,self.height)) 

        #Set Painting layers with characterisitics 
        Painting_layers = self.layers(self.layer_type, self.thickness,self.pigment, self.N_spheres, self.radius)
        print(Painting_layers)

        #Call Attenuation Class
        mu = Attenuation(self.E)

        i = 0
        for layer, q in Painting_layers.items():

            if layer.startswith(('P', 'G')):

                thickness = q['thickness']
                volume[i:i+thickness,:,:] = 0.5#mu.value('O')

                for p_i in range(len(q['pigment'])):
                    radius = q['radius'][p_i] #Because their lists 
                    N_sphere = q['N_spheres'][p_i]
                    pigment = q['pigment'][p_i]
                    print("Trou de binocchio", mu.value(pigment))
                    
                    if any(x < 2 * radius + 1 for x in (thickness, self.width, self.height)):
                        print("Error! dims of layer", x, "is too small compared with r_sphere=", radius,",radius can't be more than",(x-1)/2)
                        raise SystemExit(1)
                    else:
                        centers = self.random_insert_spheres(volume[i:i+thickness,:,:], N_sphere, radius, 1) #mu.value(pigment)
            else:
                volume[i:i+thickness,:,:]= 2#mu.value(layer)

            i += thickness

        return Painting(volume)

    @staticmethod
    def layers(layer, thickness, pigment, N_spheres, radius):

        layers_dict = {}
        for i in range(len(layer)):

            if layer[i].startswith(('P', 'G')):
                layers_dict[layer[i]] = {'thickness':thickness[i],'pigment':pigment[layer[i]],
                    'N_spheres': N_spheres[layer[i]],'radius':radius[layer[i]]} 
            else:
                layers_dict[layer[i]] = {'thickness':thickness[i]} 

        return layers_dict
    

    @staticmethod
    def random_insert_spheres(layer, nspheres, r, intensity):
        print(layer.shape)
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
                print("centers",centers)
                layer[c0-r:c0+r+1,c1-r:c1+r+1,c2-r:c2+r+1][mask] = intensity
                attempts = 0
                
        print("N_centers",len(centers))
        return centers
    

#     @staticmethod
#     def random_insert_continuous_spheres(layer, nspheres, r, intensity):
#         """Generates valid center points and insert a sphere of radius r at those points"""

#         centers = []
#         attempts = 0
#         while len(centers) < nspheres and attempts < 1000:  

#             #Generates potential center points, using boundary conditions r<=x,y,z<n-r
#             c0 = r+random.random()*(layer.shape[0]-1-2*r)
#             c1 = r+random.random()*(layer.shape[1]-1-2*r)
#             c2 = r+random.random()*(layer.shape[2]-1-2*r)
#             collision = False

#             #Check if potential center points overlap with other spheres
#             for c in centers:
#                 if (c0-c[0])**2+(c1-c[1])**2+(c2-c[2])**2 <= 4*r*r:
#                     collision=True
#                     attempts += 1
#                     break

#              if collision:
#                 continue
# th
#             # integer voxel containing the center
#             ic0, ic1, ic2 = round(c0), round(c1), round(c2)
#             oversample = 32
#             frac = Painting_generator.sphere_fraction_kernel(r,c0 - ic0,c1 - ic1,c2 - ic2,oversample)
#             layer[ic0 - r : ic0 + r + 1,ic1 - r : ic1 + r + 1, ic2 - r : ic2 + r + 1] += intensity * frac

#             centers.append((c0, c1, c2))
#             attempts = 0

#         return centers

#     @staticmethod
#     def sphere_fraction_kernel(r, cx, cy, cz, oversample=32):
#         """
#         Volume-fraction kernel for a sphere of radius r whose center is shifted by
#         (cx, cy, cz) relative to the central voxel.
#         """

#         n = 2 * r + 1

#         # voxel-center coordinates relative to sphere center
#         i = np.arange(n) - r - cx
#         j = np.arange(n) - r - cy
#         k = np.arange(n) - r - cz

#         I, J, K = np.meshgrid(i, j, k, indexing="ij")

#         # subvoxel sampling grid
#         u = (np.arange(oversample) + 0.5) / oversample - 0.5

#         dx, dy, dz = np.meshgrid(u, u, u, indexing="ij")
#         dx, dy, dz = dx.ravel(), dy.ravel(), dz.ravel()


#         # fully vectorized MC
#         x = I[..., None] + dx
#         y = J[..., None] + dy
#         z = K[..., None] + dz

#         frac = (x * x + y * y + z * z <= r * r).mean(axis=-1)

#         return frac.astype(np.float32)

