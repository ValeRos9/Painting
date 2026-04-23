import sys
import pickle
from Classes.mu import Attenuation
from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography


######## main #######
with open(sys.argv[1], "rb") as f:
    params = pickle.load(f)

#Test to see if we are in the remote 
print("Running on remote GPU server...")

#Create Painting
painting = Painting_generator(params['E'],params['pigment'],params['dim_x'], params['dim_y'], 
    params['layers'], params['N_spheres'],params['radius']).paint()
print(painting.volume)

#Generate Projection Geometry
Geom = Geometry(painting, params['SO'], params['OD'], params['n_proj'],params['geometry_type'],
    params['det_x'], params['det_y'],params['spacing_x'], params['spacing_y'])
proj_geom = Geom.projection()
#tomo_visual = Geom.tomosipo_visualization()
print(proj_geom)


#Perform Tomography 
#tomo = Tomography(painting, proj_geom, params['algorithm'])
#projections = tomo.project()
#tomo.save_projections('projections',projections)
#slices = tomo.reconstruct(projections)
#tomo.save_reconstruction('slices',slices)

#Save projection image at angle 0 
with open("projections/proj0000.tif", "rb") as f:
    data = f.read()

with open("result.pkl", "wb") as f:
    pickle.dump(data, f)
