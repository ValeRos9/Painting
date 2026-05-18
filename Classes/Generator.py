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

                if layer.startswith(('P')):
                    volume[i:i+thickness,:,:] = 0.5 #mu.value('O')
                else:
                    volume[i:i+thickness,:,:] = 0

                for p_i in range(len(q['pigment'])):
                    print('sphere',p_i)
                    radius = q['radius'][p_i]
                    N_sphere = q['N_spheres'][p_i]
                    pigment = q['pigment'][p_i]
                    
                    if any(x < 2 * radius + 1 for x in (thickness, self.width, self.height)):
                        print("Error! dims of layer", x, "is too small compared with r_sphere=", radius,",radius can't be more than",(x-1)/2)
                        raise SystemExit(1)
                    else:
                        centers = self.random_insert_spheres(volume[i:i+thickness,:,:], N_sphere, radius, 1) #mu.value(pigment)
            else:
                volume[i:i+thickness,:,:]= 0#mu.value(layer)

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
    

    # def paint(self):
    #     """generates a volume, inserts spheres and adds mu/rho values"""

    #     #Create volume
    #     total_thickness = sum(count for count in self.layers.values())
    #     volume = np.empty((total_thickness,self.width,self.height)) #I changed this 
        
    #     #Create Attenuation Class
    #     mu = Attenuation(self.E)

    #     #Index for iteration
    #     i = 0
    #     nbr = 1
    #     for typex, thickness in self.layers.items():
    #         if typex == 'P' or typex == 'G': #if you had G you get a problem with layer[tah,tah] boolean axis 0 and 3, compare 'P' with what works for 'G'
    #             print(typex)
    #             print(i,i+thickness)
                
    #             volume[i:i+thickness,:,:] = 0.5#mu.value('O')
    #             print("mu_oil",mu.value('O'))

    #             if  thickness < 2 * self.radius + 1:
    #                 print("Error! thickness of Paint or Ground layer", thickness, "is too small compared with r_sphere=", self.radius,",radius can't be more than",(thickness-1)/2)
    #                 raise SystemExit(1)
    #             else:
    #                 mu_sphere = mu.value(self.pigment[str(nbr)])
    #                 centers = self.random_insert_spheres(volume[i:i+thickness,:,:], self.N_spheres, self.radius, 1) #mu_sphere
    #                 print("pigment",self.pigment[str(nbr)])
    #                 print("mu_pigment",mu_sphere)
    #                 nbr +=1
    #         else:
    #             volume[i:i+thickness,:,:]= 0.2 #mu.value(typex)
    #             print("mu_wood",mu.value('W'))
    #         i += thickness

    #     return Painting(volume)


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
    
