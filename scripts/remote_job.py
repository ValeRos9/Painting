import sys
import pickle
from Classes.mu import Attenuation
from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography
from CT_tomosipo import Tomo


def CT_ASTRA(painting, SO, OD, n_proj,geometry_type,det_x,det_y, spacing_x, spacing_y,algorithm):
    #Generate Projection Geometry
    Geom = Geometry(painting, SO, OD, n_proj,geometry_type,det_x,det_y, spacing_x, spacing_y)
    proj_geom = Geom.projection()

    #Perform Tomography 
    tomo = Tomography(painting, proj_geom, algorithm)
    projections = tomo.project()
    tomo.save_projections('projections',projections)
    slices = tomo.reconstruct(projections)
    tomo.save_reconstruction('slices',slices)


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
CT = Tomo('standard',painting.volume,params['det_x'], params['det_y'])
A = CT.operator
projections = A(painting.volume)
print(projections.shape, type(projections[0]))
CT.save_projections('projections',projections)
reconstructions = reconstruction(projections,A)
print(reconstructions.shape)

#Classic tomography with ASTRA 
# CT_ASTRA(painting, params['SO'], params['OD'], params['n_proj'],params['geometry_type'],
#     params['det_x'], params['det_y'],params['spacing_x'], params['spacing_y'],params['algorithm'])


#Save projection image at angle 0 
with open("projections/proj0000.tif", "rb") as f:
    data = f.read()

with open("result.pkl", "wb") as f:
    pickle.dump(data, f)
