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

        volume = np.empty((sum(self.D),self.W,self.H)) 
        Layers = self.sort(self.types, self.D,self.pigment, self.N, self.a)
        mu = Attenuation(self.E)
        mu_oil = mu.value('O')

        i = 0
        for T, qty in Layers.items():
            D = qty['depth']
            vol = volume[i:i+D,:,:]

            if T.startswith(('P', 'G')):
                Pigment, N, a = qty['pigment'], qty['N'], qty['a']
                mu_pigment = mu.value(Pigment)

                for P in range(len(Pigment)):
                    if any(x < 2 * a + 1 for x in (D, self.W, self.H)):
                        print("Error! dims of layer", x, "is too small compared with r_sphere=", a,",radius can't be more than",(x-1)/2)
                        raise SystemExit(1)
   
                    vol[:] = Fraction(self.L, a, vol, N).Pigment_fraction()
                    vol[:] = vol * mu_Pigment 
                    vol[vol == 0] = mu_oil
                
            else:
                vol[:] = mu.value(T)

            i += D

        return Painting(volume)

    @staticmethod
    def sort(types, depth, pigment, N_, a):
        layers = {}
        for i, T in enumerate(types):
            layer = {'depth': depth[i]}
            if T[0] in 'PG':
                layer.update(pigment=pigment[T], N=N_[T], a=a[T])
        layers[T] = layer
        return layers 