#libraries
from __future__ import division
import numpy as np 
import random
import sys
from .Painting import Painting
from .mu import Attenuation
from .fraction import Fraction 

class Painting_generator:
    def __init__(self,E,types,pigment,H,W,D,N,a,L): 
        self.E = E
        self.types = types
        self.pigment = pigment
        self.H = H
        self.W = W
        self.D = D 
        self.N = N
        self.a = a
        self.L = L 

    def paint(self):
        """generates a volume, inserts spheres and adds mu values"""

        scale = 10000/self.L
        size = tuple(int(dim * scale) for dim in (sum(self.D), self.W, self.H))
        volume = np.empty(size) 

        Layers = self.sort(self.types, self.D,self.pigment, self.N, self.a)
        
        mu = Attenuation(self.E)
        mu_oil = mu.value('O')

        i = 0
        for T, q in Layers.items():
            D = q['depth']
            vol = volume[i:i+D,:,:]

            if T.startswith(('P', 'G')):
                Pigment, N, a = q['pigment'], q['N'], q['a']

                for P in range(len(Pigment)):
                    mu_pigment = mu.value(Pigment[P])
                    Lp = a[P]
                    Np = N[P]
                
   
                    vol[:] = Fraction(self.L, Lp, vol, Np).Pigment_fraction()
                    vol[:] = vol * mu_pigment 
                    vol[vol == 0] = mu_oil
                
            else:
                vol[:] = mu.value(T)

            i += D

        return Painting(volume)

    @staticmethod
    def sort(types, depth, pigment, N, a):
        layers = {}
        for i, T in enumerate(types):
            layer = {'depth': depth[i]}
            if T[0] in 'PG':
                layer.update(pigment=pigment[T], N=N[T], a=a[T])
        layers[T] = layer
        return layers 












#libraries
# from __future__ import division
# import numpy as np 
# import random
# import sys
# from .Painting import Painting
# from .mu import Attenuation

# class Painting_generator:
#     def __init__(self,E,layer_type,pigment,height,width,thickness,N_spheres,radius): 
#         self.E = E
#         self.layer_type = layer_type
#         self.pigment = pigment
#         self.height = height
#         self.width = width
#         self.thickness = thickness 
#         self.N_spheres = N_spheres 
#         self.radius = radius

#     def paint(self):
#         """generates a volume, inserts spheres and adds mu values"""

#         #Generate Painting volume
#         volume = np.empty((sum(self.thickness),self.width,self.height)) 

#         #Set Painting layers with characterisitics 
#         Painting_layers = self.layers(self.layer_type, self.thickness,self.pigment, self.N_spheres, self.radius)
#         print(Painting_layers)

#         #Call Attenuation Class
#         mu = Attenuation(self.E)

#         i = 0
#         for layer, q in Painting_layers.items():

#             if layer.startswith(('P', 'G')):

#                 thickness = q['thickness']
#                 volume[i:i+thickness,:,:] = 0.5#mu.value('O')

#                 for p_i in range(len(q['pigment'])):
#                     radius = q['radius'][p_i] #Because their lists 
#                     N_sphere = q['N_spheres'][p_i]
#                     pigment = q['pigment'][p_i]
#                     print("Trou de binocchio", mu.value(pigment))
                    
#                     if any(x < 2 * radius + 1 for x in (thickness, self.width, self.height)):
#                         print("Error! dims of layer", x, "is too small compared with r_sphere=", radius,",radius can't be more than",(x-1)/2)
#                         raise SystemExit(1)
#                     else:
#                         centers = self.random_insert_spheres(volume[i:i+thickness,:,:], N_sphere, radius, 1) #mu.value(pigment)
#             else:
#                 print(layer)
#                 volume[i:i+thickness,:,:]= mu.value(layer)

#             i += thickness

#         return Painting(volume)

#     @staticmethod
#     def layers(layer, thickness, pigment, N_spheres, radius):

#         layers_dict = {}
#         for i in range(len(layer)):

#             if layer[i].startswith(('P', 'G')):
#                 layers_dict[layer[i]] = {'thickness':thickness[i],'pigment':pigment[layer[i]],
#                     'N_spheres': N_spheres[layer[i]],'radius':radius[layer[i]]} 
#             else:
#                 layers_dict[layer[i]] = {'thickness':thickness[i]} 

#         return layers_dict
    

#     @staticmethod
#     def random_insert_spheres(layer, nspheres, r, intensity):
#         print(layer.shape)
#         """Generates valid center points and insert a sphere of radius r at those points"""

#         #Creates a box with at center a standard sphere of radius r
#         x,y,z = np.meshgrid(np.arange(2*r+1), np.arange(2*r+1), np.arange(2*r+1), indexing='ij')
#         mask = (x - r)**2 + (y - r)**2 + (z - r)**2  <= r**2

#         centers = []
#         attempts = 0
#         while len(centers) < nspheres and attempts < 1000:  

#             #Generates potential center points, using boundary conditions r<=x,y,z<n-r
#             c0 = round(r+random.random()*(layer.shape[0]-1-2*r))
#             c1 = round(r+random.random()*(layer.shape[1]-1-2*r))
#             c2 = round(r+random.random()*(layer.shape[2]-1-2*r))
#             collision = False

#             #Check if potential center points overlap with other spheres
#             for c in centers:
#                 if (c0-c[0])**2+(c1-c[1])**2+(c2-c[2])**2 <= 4*r*r:
#                     collision=True
#                     attempts += 1
#                     break

#             if not collision:
#                 centers.append((c0,c1,c2))
#                 print("centers",centers)
#                 layer[c0-r:c0+r+1,c1-r:c1+r+1,c2-r:c2+r+1][mask] = intensity
#                 attempts = 0
                
#         print("N_centers",len(centers))
#         return centers
    

