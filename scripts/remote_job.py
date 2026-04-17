import sys
import pickle

from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography


def run_remote(params):

    #Test to see if we are in the remote 
    print("Running on remote GPU server...")

    # 1. Create Painting
    painting = Painting_generator(params['dim_x'], params['dim_y'], params['thickness'],
        params['layers_val'], params['N_spheres'],params['radius'], params['sphere_val']).paint()

    print(painting)

    # 2. Generate projection Geometry
    proj_geom = Geometry(painting, params['SO'], params['OD'], params['n_proj'],params['geometry_type'],
        params['det_x'], params['det_y'],params['spacing_x'], params['spacing_y']).projection()

    # 3. Perform projections and reconstructions 
    tomo = Tomography(painting, proj_geom, params['algorithm'])
    projections = tomo.project()
    tomo.save_projections('projections',projections)
    #slices = tomo.reconstruct(projections)
    #tomo.save_reconstruction('slices',slices)

    # 4. Save projection image  
    with open("result.pkl", "wb") as f:
        pickle.dump(projections[0], f)


with open(sys.argv[1], "rb") as f:
    params = pickle.load(f)

run_remote(params)
