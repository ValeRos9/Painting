import sys
import pickle
from Classes.mu import Attenuation
from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography
from CT_tomosipo import Tomo


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
CT_tomosipo = Tomo(painting.volume,'standard',params['det_x'], params['det_y'])
A = CT_tomosipo.operator()
projections = A(painting.volume)

print(f"Shape: {projections.shape}")
print(f"Type: {projections.dtype}")
print(f"Expected shape logic: Angles={projections.shape[0] if len(projections.shape)==3 else 'Unknown'}, DetY={projections.shape[1]}, DetX={projections.shape[2]}")
print(projections.shape)

CT_tomosipo.save_projections('projections',projections)
slices = CT.reconstruction(projections,A)
CT_tomosipo.save_reconstruction('slices',slices)
print(slices.shape)


#Save projection image at angle 0 
with open("projections/proj0000.tif", "rb") as f:
    data = f.read()

with open("result.pkl", "wb") as f:
    pickle.dump(data, f)


