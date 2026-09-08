import numpy as np 
import random

def insert_mu(Volume):
    mu_pigment = 1
    mu_oil = 0
    Volume[:] = Volume * mu_pigment + Volume[Volume==0] * mu_oil

#Generate valid center points 
def Generate_spheres(nb_type, layer, N, h):
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

#Picks case for volume fraction pigment_length to voxel length
def Pigment_fraction(L,a,Volume):
    a_corr = a/L
    h = a_corr/2

    if L > 4 * a:
        n = 1 #n should be some kind of mask (NXNxN)
        f = (a_corr**3) * n
        Volume[...] = f
    
    elif (4 * a >= L) and (L >= a):
        Ns=10000
        centers = Generate_spheres("real",Volume, Ns, h)
        fraction_tilda(Volume,centers,h)

    else:
        Ns=2
        centers = Generate_spheres("integers",Volume, Ns, h)
        h = round(h)
        for c in centers:
            f = 1 
            Volume[c[0]-h:c[0]+h+1,c[1]-h:c[1]+h+1,c[2]-h:c[2]+h+1] = f

#Computes partial length of the cube per axis intersection
def intersection_length(v, c, s, h):
    dist = np.empty((len(v),2))
    dist[:, 0] = np.where(s == 1, (v + 0.5) - (c - h), (c + h) - (v - 0.5))
    dist[:, 1] = np.where(s == 1, (c + h) - (v + 0.5), (v - 0.5) - (c - h))
    return dist

#Computes volume fraction for pigment ~ voxel
def fraction_tilda(Volume,centers,h):
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
            
    

#Initialize 
Volume = np.zeros((1000,1000,1000))
a = 10 #microns
L = 40 # microns

#Run 
Pigment_fraction(L,a,Volume)


#1. Modify Generator, incoporate this file
#2. Check if it works
#3. Combine with workstation

# 2) There is no need to change the sampling within tomosipo, tomosipo only tells you what size this voxelisation established within painting generator needs to be
#4. Configure workstation to LIACS network 
#5. Modify the code in local and remote 