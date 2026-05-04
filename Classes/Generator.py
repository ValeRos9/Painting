#libraries
from __future__ import division
import numpy as np 
import random
import sys
from .Painting import Painting
from .mu import Attenuation


class Painting_generator:
    def __init__(self,E,pigment,height,width,layers,N_spheres,radius):
        self.E = E
        self.pigment = pigment
        self.height = height
        self.width = width
        self.layers = layers #this is a dict 
        self.N_spheres = N_spheres 
        self.radius = radius

    def paint(self):
        """generates a volume, inserts spheres and adds mu/rho values"""

        #Create volume
        total_thickness = sum(count for count in self.layers.values())
        volume = np.empty((total_thickness,self.width,self.height)) #I changed this 

        i = 0
        mu_rho = Attenuation(self.E)
        for typex, thickness in self.layers.items():
            
            if typex == 'P':
                volume[i:i+thickness,:,:] = 0.5#mu_rho.value('O')
                #print("mu_oil",mu_rho.value('O'))

                if i+thickness < 2 * self.radius + 1:
                    print("Error! thickness of Paint layer", i+thickness, "is too small compared with r_sphere=", self.radius,",radius can't be more than",(i+thickness-1)/2)
                    raise SystemExit(1)
                else:
                    #insert spheres with value mu/rho_sphere 
                    centers = self.random_insert_spheres(volume[i:i+thickness,:,:], self.N_spheres, self.radius, 1) #mu_rho.value(self.pigment)
                    #print("mu_pigment",mu_rho.value(self.pigment))
            else:
                #Remember your missing the ground layer value, and you need to put typex
                #mu.value(typex) not mu.value('W')
                volume[i:i+thickness,:,:]= 0.2#mu_rho.value('W')
                #print("mu_wood",mu_rho.value('W'))

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
