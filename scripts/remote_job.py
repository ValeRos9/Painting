import sys
import pickle
from Classes.mu import Attenuation
from Classes.Generator import Painting_generator
from CT_tomosipo import Tomo
import numpy as np
from scipy.ndimage import zoom

######## main #######
with open(sys.argv[1], "rb") as f:
    params = pickle.load(f)

#Test to see if we are in the remote 
print("Running on remote GPU server...")

#Create Painting
painting = Painting_generator(params['E'],params['pigment'],params['dim_x'], params['dim_y'], 
    params['layers'], params['N_spheres'],params['radius']).paint()
print(painting.volume.shape)

#CT with tomosipo
det_row = params['det_x']
det_col = params['det_y']
n_proj = params['n_proj']
SO = params['SO']
OD = params['OD']
Nx = 256
Ny = 256
slices = 100

CT_tomosipo = Tomo(painting.volume,n_proj,det_row,det_col,SO,OD,Nx,Ny,slices)

A = CT_tomosipo.operator()

projections = CT_tomosipo.projections(A)
CT_tomosipo.save_projections('projections',projections)

slices = CT_tomosipo.reconstruction(projections,A)
CT_tomosipo.save_reconstruction('slices',slices)
print(slices.shape)


#Save projection image at angle 0 
with open("projections/proj0000.tif", "rb") as f:
    data = f.read()

with open("result.pkl", "wb") as f:
    pickle.dump(data, f)


