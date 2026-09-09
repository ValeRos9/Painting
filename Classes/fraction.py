import numpy as np 
import random

class Fraction:
    def __init__(self,L,a,Volume,N): 
        self.L = L
        self.a = a
        self.Volume = Volume
        self.N = N

    def Pigment_fraction(self):
        """
        Checks voxel length vs Pigment length, and chooses Volume Fraction scheme 
        """
        a_corr = self.a/self.L
        h = a_corr/2

        if self.L > 4 * self.a:
            n = 1 #n should be some kind of mask (NXNxN)
            f = (a_corr**3) * n
            self.Volume[...] = f
    
        elif (4 * a >= L) and (L >= a):
            centers = Generate_centers("real",self.Volume, self.N, h)
            fraction_tilda(self.Volume,centers,h)

        else:
            centers = Generate_centers("integers",self.Volume, self.N, h)
            h = round(h)
            for c in centers:
                f = 1 
                self.Volume[c[0]-h:c[0]+h+1,c[1]-h:c[1]+h+1,c[2]-h:c[2]+h+1] = f



    @staticmethod 
    def Generate_centers(nb_type, layer, N, h):
        """
        Generate valid center points for the cube-shaped pigment: center c, length a , half-length h 
        """
        centers = np.empty((N, 3))
        n = 0
        attempts = 0
        while n < N and attempts < 1000:
            c = np.array([h + random.random() * (s - 1 - 2*h) for s in layer.shape]) 
            collision = np.any(np.all(np.abs(c - centers[:n]) <= 2*h, axis=1))

            if  n > 0 and collision:
                attempts += 1
            else:
                centers[n] = c
                n += 1
                attempts = 0

        if nb_type == "integers":
                centers = centers.astype(int)
        return centers[:n]

    @staticmethod 
    def fraction_tilda(Volume,centers,h):
        """
        Computes volume fraction for pigment ~ voxel
        """
        for c in centers:
            v = np.round(c) #closest voxel
            s = np.sign(c-v) #orientation
            d = s * np.where(s==1, v+0.5<c+h , v-0.5>c-h).astype(int) #check if axis is intersected

            index = d != 0 
            N_int = np.count_nonzero(index)
            a = 2 * h
            
            if N_int == 0:
                f = np.array([(a)**3])
                voxels = np.array([v])

            else:
                Length = intersection_length(v[index], c[index], s[index], h) 
                
                if N_int == 1:
                    f = (np.array(Length)).ravel() * (a**2)
                    voxels = np.array([v, v + d])

                elif N_int ==2:
                    d0,d1 = np.eye(3, dtype=int)[index] * d[index,None]
                    f = np.einsum('i,j->ji', *Length).ravel() * a
                    voxels = v + np.array([[0,0,0], d0, d1, d])
        
                else:
                    d0,d1,d2 = np.eye(3, dtype=int)[index] * d[index,None]
                    f = np.einsum('i,j,k->kji', *Length).ravel()
                    voxels = v + np.array([[0,0,0], d0, d1, d0+d1, d2, d2+d0, d2+d1, d])

            Volume[voxels[:, 0].astype(int), voxels[:, 1].astype(int), voxels[:, 2].astype(int)] += f

                
    @staticmethod 
    def intersection_length(v, c, s, h):
        """
        Computes partial length of the cube per axis intersection
        """
        dist = np.empty((len(v),2))
        dist[:, 0] = np.where(s == 1, (v + 0.5) - (c - h), (c + h) - (v - 0.5))
        dist[:, 1] = np.where(s == 1, (c + h) - (v + 0.5), (v - 0.5) - (c - h))
        return dist

#1. voxel length vs pixel length of detector, i think here u have sthg interesting to think about 
#2. Where do u put Tomosipo and understand scripts, info, how this is setup
#3. Change the Github 

#1. I would start by making sure that Painting gets generated properly for all 3 cases.
#2. I would check that a simulation works
#3. I would understand the relationship between voxel length of volume and pixel length of detector, what freedom this gives u 
#4. I would look into ESRF example to get the coordinates and study the figure, same with Rijksmuseum
#5. Understand how the repo is setup, change CT_tomosipo, and Github