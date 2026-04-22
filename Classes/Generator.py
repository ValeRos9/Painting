#libraries
from __future__ import division
import numpy as np 
import random
import sys
from .Painting import Painting
from .mu import Attenuation

class Painting_generator:
    def __init__(self,E,pigment,dim_x,dim_y,layers,N_spheres,radius):
        self.E = E
        self.pigment = pigment
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.layers = layers #this is a dict 
        self.N_spheres = N_spheres 
        self.radius = radius

    def paint(self):
        """generates a volume, inserts spheres and adds mu/rho values"""

        print(self.layers)

        #Create volume
        total_thickness = sum(count for count in self.layers.keys())
        volume = np.empty((total_thickness,self.dim_y,self.dim_x))

        for typex, thickness in layers.items():
            i = 0
            if typex == 'P':
                #mu_oil = mu[typex] = Attenuation(self.E, =).=()
                mu_rho_oil = 3
                volume[i:i+thickness,:,:] = mu_rho_oil
                if i+thickness < 2 * self.radius + 1:
                    print("Error! thickness of Paint layer", i+thickness, "is too small compared with r_sphere=", self.radius,",radius can't be more than",(i+thickness-1)/2)
                    raise SystemExit(1)
                else:
                    #insert spheres with value mu/rho_sphere 
                    mu_rho_sphere = Attenuation(self.E, self.pigment).value() 
                    centers = self.random_insert_spheres(volume[i:i+thickness,:,:], self.N_spheres, self.radius, mu_rho_sphere)

                    i += thickness
            else:
                mu_rho_whatever = 2
                volume[i:i+thickness,:,:]=mu_rho_whatever

                i += thickness

        return Painting(volume)


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
class Painting_generator:
    def __init__(self,dim_x,dim_y,thickness,layers_val,N_spheres,radius,sphere_val):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.thickness = thickness
        self.layers_val = layers_val
        self.N_spheres = N_spheres 
        self.radius = radius
        self.sphere_val = sphere_val
    
    def paint(self):
        creates a Painting, generating volume, inserting spheres and adding intensity values

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
        Generates valid center points and insert a sphere of radius r at those points

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
